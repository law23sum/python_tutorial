import litellm
from asgiref.sync import async_to_sync
from celery import shared_task

from apps.chat.models import Chat, MessageTypes
from apps.chat.prompts import get_chat_naming_prompt
from apps.chat.serializers import ChatMessageSerializer
from apps.chat.sessions import get_session
from apps.chat.utils import get_llm_kwargs


@shared_task(bind=True)
def get_chat_response(self, chat_id: int, message: str) -> str:
    chat = Chat.objects.get(id=chat_id)
    session = get_session(chat)

    response = async_to_sync(session.get_response)()
    message = async_to_sync(session.save_message)(response, MessageTypes.AI)
    return ChatMessageSerializer(message).data


@shared_task
def set_chat_name(chat_id: int, message: str):
    chat = Chat.objects.get(id=chat_id)
    if not message:
        return
    elif len(message) < 30:
        # for short messages, just use them as the chat name. the summary won't help
        chat.name = message
        chat.save()
    else:
        # set the name with openAI
        messages = [
            {"role": "developer", "content": get_chat_naming_prompt()},
            {"role": "user", "content": f"Summarize the following text: '{message}'"},
        ]
        response = litellm.completion(messages=messages, **get_llm_kwargs())
        chat.name = response.choices[0].message.content[:100].strip()
        chat.save()
