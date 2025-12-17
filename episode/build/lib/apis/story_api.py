from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import ORJSONResponse

from story_registry import stories
from models.story import Stories, Story, StoryPayload, StoryMetadata

from logic.agent_manager import AgentManager


router = APIRouter()
agent_manager = AgentManager()


@router.get("/stories")
async def get_stories():

    story_model = Stories(data=list(Story(**story) for story in stories.values()))
    return story_model


@router.post("/stories/next")
async def post_next(payload: StoryPayload = Body(...)):
    agent = await agent_manager.get_agent(payload.story_id, payload.session_id)
    result = await agent.generate_next(payload.user_choice)
    return result


@router.get("/stories/{story_id}")
async def get_story_by_id(story_id: str):
    """
    Get story metadata and extended description by ID.
    No narration or agent creation happens here.
    """
    if story_id not in stories:
        raise HTTPException(status_code=404, detail="Story not found")

    story_info = Story(**stories[story_id])

    # Add a longer description (could also come from a file or registry)
    extended_description = (
        f"{story_info.description}\n\n"
        f"This story will take you through {story_info.genre} adventures across "
        f"{story_info.episode_count} thrilling episodes. "
        "Every choice you make shapes the path ahead, and no two journeys are alike."
    )

    return ORJSONResponse(
        status_code=200,
        content=StoryMetadata(
            metadata=story_info,
            detailedDescription=extended_description,
        ).model_dump(),
    )
