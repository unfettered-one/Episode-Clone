from typing import Annotated

from pydantic import BaseModel, Field


class Story(BaseModel):
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }
    id: str
    title: str
    description: str
    story_path: str
    author: str | None = None
    episode_count: str | None = "32"
    cover_image: str | None = None
    likes: str | None = "3200"
    views: str | None = "64000"
    genre: str | None = "Drama"


class Stories(BaseModel):
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }
    data: list[Story]


class StoryPayload(BaseModel):
    story_id: Annotated[str, Field(alias="storyId")]
    user_choice: Annotated[str, Field(alias="userChoice")]
    # session_id: str
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }


class StoryMetadata(BaseModel):
    metadata: Story
    detailedDescription: str
