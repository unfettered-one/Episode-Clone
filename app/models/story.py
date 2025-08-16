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


class Stories(BaseModel):
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }
    data: list[Story]


class StoryPayload(BaseModel):
    story_id: str = Field(alias="storyId")
    user_choice: str = Field(alias="userChoice")
    session_id: str = Field(alias="sessionId")
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }
