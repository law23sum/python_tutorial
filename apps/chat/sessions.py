from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

import litellm

from apps.ai.agents import AgentTypes, get_agent, run_agent, run_agent_streaming
from apps.ai.handlers import agent_event_stream_handler
from apps.chat.models import Chat, ChatMessage, ChatTypes, MessageTypes
from apps.chat.prompts import get_default_system_prompt
from apps.chat.utils import get_llm_kwargs
from apps.users.models import CustomUser


class ChatSessionBase(ABC):
    """Base class for chat sessions that is used by consumers"""

    user: CustomUser
    chat_type: ChatTypes
    agent_type: AgentTypes | None = None
    chat: Chat | None = None
    messages: list[dict] = []
    # Whether chunks are cumulative ("the", "the boy", "the boy is"...)
    # or incremental ("the", "boy", "is"...)
    # this impacts how they should be rendered in the UI
    cumulative_streaming: bool = False

    def __init__(self, user: CustomUser, chat_type: ChatTypes, chat_id: int | None):
        self.user = user
        self.chat_type = chat_type
        self.chat_id = chat_id
        self.messages = []
        system_prompt = self.get_system_prompt()
        if system_prompt:
            self.messages.append(
                {
                    "role": "developer",
                    "content": system_prompt,
                }
            )

    async def _async_init(self):
        if self.chat_id:
            self.chat = await Chat.objects.aget(user=self.user, id=self.chat_id)
            self.messages.extend([m.to_openai_dict() async for m in ChatMessage.objects.filter(chat=self.chat)])
        else:
            self.chat = None

    @classmethod
    def from_chat(cls, chat: Chat) -> "ChatSessionBase":
        session = cls(chat.user, chat.chat_type, chat.id)
        session.chat = chat
        session.messages.extend([m.to_openai_dict() for m in ChatMessage.objects.filter(chat=chat)])
        return session

    @classmethod
    async def create(cls, user: CustomUser, chat_type: ChatTypes, chat_id: int | None):
        session = cls(user=user, chat_type=chat_type, chat_id=chat_id)
        await session._async_init()
        return session

    async def add_message(self, message_text: str) -> tuple[ChatMessage, bool]:
        """
        Returns whether the chat was created.
        """
        from apps.chat.tasks import set_chat_name

        # if no chat set, create one and set the name
        chat_created = False
        if not self.chat:
            chat_created = True
            chat_kwargs = {
                "user": self.user,
                "chat_type": self.chat_type,
            }
            if self.agent_type:
                chat_kwargs["agent_type"] = self.agent_type

            if len(message_text) < 40:
                chat_kwargs["name"] = message_text
                self.chat = await Chat.objects.acreate(**chat_kwargs)
            else:
                self.chat = await Chat.objects.acreate(**chat_kwargs)
                # only try to set the chat name with AI if the message is long enough
                set_chat_name.delay(self.chat.id, message_text)

        message = await self.save_message(message_text, MessageTypes.HUMAN)
        return message, chat_created

    async def save_message(self, message_text: str, message_type: MessageTypes) -> ChatMessage:
        # save the user's message to the DB
        message = await ChatMessage.objects.acreate(
            chat=self.chat,
            message_type=message_type,
            content=message_text,
        )
        self.messages.append(message.to_openai_dict())
        return message

    @abstractmethod
    def get_system_prompt(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_response(self) -> str:
        """Return the next message in the chat from the session's current set of messages."""
        raise NotImplementedError

    @abstractmethod
    async def get_response_streaming(self) -> AsyncGenerator[str, None]:
        """Return message chunks as strings for streaming."""
        raise NotImplementedError


class ChatSession(ChatSessionBase):
    def get_system_prompt(self) -> str | None:
        return get_default_system_prompt()

    async def get_response(self) -> str:
        """Return message chunks as strings for streaming."""
        response = litellm.completion(
            messages=self.messages,
            **get_llm_kwargs(),
        )
        return response.choices[0].message.content.strip()

    async def get_response_streaming(self) -> AsyncGenerator[str, None]:
        """Return message chunks as strings for streaming."""
        response_stream = await litellm.acompletion(messages=self.messages, stream=True, **get_llm_kwargs())
        async for chunk in response_stream:
            message_chunk = chunk.choices[0].delta.content
            if message_chunk:
                yield message_chunk


class AgentSession(ChatSessionBase):
    # Agent streaming returns cumulative chunks, so we need to replace entire content
    cumulative_streaming: bool = True

    def __init__(self, user: CustomUser, chat_type: ChatTypes, chat_id: int | None, agent_type: AgentTypes):
        super().__init__(user, chat_type, chat_id)
        self.agent_type = agent_type
        self.agent = get_agent(agent_type)

    @classmethod
    def from_chat(cls, chat: Chat) -> "ChatSessionBase":
        session = cls(chat.user, chat.chat_type, chat.id, chat.agent_type)
        session.chat = chat
        session.messages.extend([m.to_openai_dict() for m in ChatMessage.objects.filter(chat=chat)])
        return session

    def get_system_prompt(self) -> str | None:
        # agent system prompts are managed by the agents themselves
        return None

    async def get_response(self) -> str:
        """Return the next message in the chat from the session's current set of messages."""

        response = await run_agent(
            self.agent,
            self.user,
            self.messages[-1]["content"],
            message_history=self.messages[:-1],
            event_stream_handler=agent_event_stream_handler,
        )
        return response

    async def get_response_streaming(self) -> AsyncGenerator[str, None]:
        """Return message chunks as strings for streaming."""
        # Pass all messages in the conversation history, not just the last one
        # The first message is the system prompt, followed by the conversation history
        # We pass all messages except the current user message (which is the last one)
        # The current user message will be passed as the 'message' parameter to run_agent
        message_history = self.messages[:-1]  # All messages except the current user message

        async for chunk in run_agent_streaming(
            self.agent,
            self.user,
            self.messages[-1]["content"],
            message_history=message_history,
            event_stream_handler=agent_event_stream_handler,
        ):
            yield chunk


def get_session_class(chat_type: ChatTypes) -> type[ChatSessionBase]:
    if chat_type == ChatTypes.CHAT:
        return ChatSession
    elif chat_type == ChatTypes.AGENT:
        return AgentSession
    else:
        raise ValueError(f"Invalid chat type: {chat_type}")


def get_session(chat: Chat) -> ChatSessionBase:
    session_class = get_session_class(chat.chat_type)
    return session_class.from_chat(chat)
