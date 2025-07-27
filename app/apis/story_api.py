from fastapi import APIRouter, Body

from story_registry import stories
from models.story import Stories, Story, StoryPayload

from logic.agent_manager import AgentManager


router = APIRouter()
agent_manager = AgentManager()


@router.get("/stories")
async def get_stories():

    story_model = Stories(data=list(Story(**story) for story in stories.values()))
    return story_model


@router.post("/stories/next")
async def post_next(payload: StoryPayload = Body(...)):
    agent = await agent_manager.get_agent(payload.story_id, "default")
    result = await agent.generate_next(payload.user_choice)
    return result
