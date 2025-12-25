from fastapi import APIRouter, Body, Security
from fastapi.responses import ORJSONResponse

from episode.story_registry import stories
from episode.models.story import Stories, Story, StoryPayload, StoryMetadata
from episode.security.auth import verify_access_token
from episode.logic.agent_manager import AgentManager

from errorhub.decorator import api_exception_handler
from errorhub.exceptions import NotFoundException
from errorhub.models import ErrorSeverity

router = APIRouter()


@router.get("/stories")
@api_exception_handler
async def get_stories(token_data=Security(verify_access_token)):

    story_model = Stories(data=list(Story(**story) for story in stories.values()))
    return story_model


@router.post("/stories/next")
@api_exception_handler
async def post_next(
    payload: StoryPayload = Body(...),
):
    # token_data=Security(verify_access_token)):
    agent_manager = AgentManager()
    agent = await agent_manager.get_agent(payload.story_id, "123")
    result = await agent.generate_next(payload.user_choice)
    return result


@router.get("/stories/{story_id}")
@api_exception_handler
async def get_story_by_id(story_id: str, token_data=Security(verify_access_token)):
    """
    Get story metadata and extended description by ID.
    No narration or agent creation happens here.
    """
    if story_id not in stories:
        raise NotFoundException(
            service="Episode Game",
            severity=ErrorSeverity.LOW,
            message="Story not found",
            context={"story_id": story_id},
        )

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
