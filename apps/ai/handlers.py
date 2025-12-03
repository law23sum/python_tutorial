import logging
from collections.abc import AsyncIterable

from pydantic_ai.messages import (
    AgentStreamEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
)

logger = logging.getLogger("pegasus.ai")


async def agent_event_stream_handler(ctx, event_stream: AsyncIterable[AgentStreamEvent]):
    """Handle and log agent execution events for debugging."""
    async for event in event_stream:
        # log any instances of tool calls and results
        if isinstance(event, FunctionToolCallEvent):
            logger.debug(f"🔧 LLM calls tool={event.part.tool_name!r} with args={event.part.args}")
        elif isinstance(event, FunctionToolResultEvent):
            logger.debug(f"✅ Tool call {event.tool_call_id!r} returned => {event.result.content}")
