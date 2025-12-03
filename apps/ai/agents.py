from __future__ import annotations as _annotations

from enum import StrEnum

from django.conf import settings
from django.utils import timezone
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    TextPart,
    UserPromptPart,
)
from pydantic_ai.toolsets import AbstractToolset

from apps.ai.tools import admin_db, email_toolset, employee_toolset, weather_toolset
from apps.ai.types import UserDependencies
from apps.chat.prompts import get_default_system_prompt
from apps.users.models import CustomUser


async def add_user_name(ctx: RunContext[UserDependencies]) -> str:
    return f"The user's name is {ctx.deps.user.get_display_name()}"


async def add_user_email(ctx: RunContext[UserDependencies]) -> str:
    return f"The user's email is {ctx.deps.user.email}"


async def current_datetime(ctx: RunContext[UserDependencies]) -> str:
    return f"The current datetime is {timezone.now()}"


DEFAULT_INSTRUCTIONS = [get_default_system_prompt(), add_user_name, add_user_email, current_datetime]


class AgentTypes(StrEnum):
    WEATHER = "weather"
    ADMIN = "admin"
    EMPLOYEES = "employees"


def get_agent(agent_type: AgentTypes):
    if agent_type == AgentTypes.WEATHER:
        return get_weather_agent()
    elif agent_type == AgentTypes.ADMIN:
        return get_admin_agent()
    elif agent_type == AgentTypes.EMPLOYEES:
        return get_employees_agent()
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")


def get_weather_agent():
    return _get_agent([weather_toolset])


def get_admin_agent():
    return _get_agent([admin_db, email_toolset])


def get_employees_agent():
    return _get_agent([employee_toolset])


def _get_agent(toolsets: list[AbstractToolset]):
    return Agent(
        settings.DEFAULT_AGENT_MODEL,
        toolsets=toolsets,
        instructions=DEFAULT_INSTRUCTIONS,
        retries=2,
        deps_type=UserDependencies,
    )


def convert_openai_to_pydantic_messages(openai_messages: list[dict]) -> list[ModelMessage]:
    """Convert OpenAI-style messages to Pydantic AI ModelMessage format."""
    pydantic_messages = []

    for msg in openai_messages:
        role = msg.get("role")
        content = msg.get("content")

        if role == "user":
            pydantic_messages.append(ModelRequest(parts=[UserPromptPart(content=content)]))
        elif role == "assistant":
            pydantic_messages.append(ModelResponse(parts=[TextPart(content=content)]))
        elif role in ["system", "developer"]:
            pydantic_messages.append(ModelRequest(parts=[SystemPromptPart(content=content)]))

    return pydantic_messages


async def run_agent(
    agent: Agent, user: CustomUser, message: str, message_history: list[dict] = None, event_stream_handler=None
):
    """Run an agent and return the response."""
    deps = UserDependencies(user=user)
    pydantic_messages = convert_openai_to_pydantic_messages(message_history) if message_history else None
    result = await agent.run(
        message, message_history=pydantic_messages, deps=deps, event_stream_handler=event_stream_handler
    )
    return result.output


async def run_agent_streaming(
    agent: Agent, user: CustomUser, message: str, message_history: list[dict] = None, event_stream_handler=None
):
    """Run an agent and stream the response."""
    deps = UserDependencies(user=user)
    pydantic_messages = convert_openai_to_pydantic_messages(message_history) if message_history else None
    async with agent.run_stream(
        message, message_history=pydantic_messages, deps=deps, event_stream_handler=event_stream_handler
    ) as result:
        async for text in result.stream_text():
            yield text
