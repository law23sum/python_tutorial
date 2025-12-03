from pydantic import BaseModel
from pydantic_ai import RunContext
from pydantic_ai.toolsets import FunctionToolset

from apps.ai.types import UserDependencies
from tutorial.apps.topics.registry import TOPICS, get_topic


class TopicData(BaseModel):
    slug: str
    title: str
    summary: str

    @classmethod
    def from_registry(cls, slug: str) -> "TopicData":
        topic = get_topic(slug)
        return cls(slug=topic["slug"], title=str(topic["title"]), summary=str(topic["summary"]))


def list_topics(ctx: RunContext["UserDependencies"]) -> list[TopicData]:
    """Return every tutorial topic."""

    return [TopicData.from_registry(topic["slug"]) for topic in TOPICS]


def get_topic_details(ctx: RunContext["UserDependencies"], slug: str) -> TopicData:
    """Return a single tutorial topic by slug."""

    return TopicData.from_registry(slug)


topics_toolset = FunctionToolset(
    tools=[
        list_topics,
        get_topic_details,
    ]
)
