import json
import logging

from episode.logic.faiss_index import FaissIndex
from episode.logic.gemini_magic import gemini

from episode.utils.history_manager import history_manager
from episode.story_registry import stories
from episode.configuration import settings

from errorhub.exceptions import InternalServerErrorException
from errorhub.models import ErrorSeverity

LOGGER = logging.getLogger(__name__)


class StoryRAGAgent:
    def __init__(self, story_id: str, session_id: str):
        if story_id not in stories:
            raise InternalServerErrorException(
                service="Episode",
                message=f"Story ID '{story_id}' not found in registry.",
                severity=ErrorSeverity.MEDIUM,
            )

        self.story_id = story_id
        self.story_info = stories[story_id]
        self.faiss_index = FaissIndex()
        self.session_id = session_id
        self.user_story_id = self.story_id + "-" + self.session_id

    async def generate_next(self, user_choice: str) -> dict:
        """
        Generate next story turn based on user's choice.
        Combines static folklore with dynamic recent history from DynamoDB.
        """
        # Build prompt with folklore + recent history from DynamoDB
        prompt = await self._generate_prompt_for_agent(user_choice)

        # Get AI response
        response = await gemini.generate_response(prompt)
        cleaned_response = await self._convert_ai_response_text_to_json(response)

        # Get next turn number and save to DynamoDB
        turn_number = await history_manager.increment_turn_count(self.user_story_id)
        await history_manager.save_turn(self.user_story_id, turn_number, user_choice, cleaned_response)

        return {"response": cleaned_response}

    async def _convert_ai_response_text_to_json(self, ai_response: str) -> dict:
        # Convert the AI response text to JSON format
        cleaned = ai_response.strip().replace("```json", "").replace("```", "").strip()
        json_response = json.loads(cleaned)
        return json_response

    async def _get_last_n_turns_from_db(self, n: int) -> list[dict]:
        """
        Read last N turns from DynamoDB.
        Returns list of dicts with 'choice' and 'narration'.
        """
        return await history_manager.get_last_n_turns(self.user_story_id, n)

    async def _format_turns_as_history_text(self, turns: list[dict]) -> str:
        """
        Format turns into readable history text for the prompt.
        """
        if not turns:
            return ""

        history_lines = []
        for i, turn in enumerate(turns, 1):
            history_lines.append(f"Turn {i}:")
            history_lines.append(f"  Player chose: {turn['choice']}")
            history_lines.append(f"  What happened: {turn['narration']}")
            history_lines.append("")  # Blank line between turns

        return "\n".join(history_lines)

    async def _get_history_text(self, n: int) -> str:
        """
        Get formatted history text from last N turns stored in DynamoDB.
        """
        turns = await self._get_last_n_turns_from_db(n)
        return await self._format_turns_as_history_text(turns)

    async def _get_story_context_from_faiss_index(self, user_choice: str) -> str:
        """
        Retrieve static story folklore and world-building context.
        Queries base story only (not user session).
        """
        query = await self._build_folklore_query(user_choice)
        # Query BASE story ID, not user session - folklore is static
        docs = await self.faiss_index.similarity_search(query, self.story_id, top_chunks=4)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    async def _build_folklore_query(self, user_choice: str) -> str:
        """
        Build query to retrieve relevant world-building and character context.
        Focus on static story elements, not dynamic gameplay.
        """
        return f"Story world context, characters, and lore relevant to: {user_choice}"

    async def _generate_prompt_for_agent(self, user_choice: str) -> str:
        """
        Build prompt combining:
        1. Static story folklore (from vector DB)
        2. Recent gameplay history (last 3 turns)
        3. Current user choice
        """
        # Get static world context from vector DB (folklore, characters, lore)
        story_folklore = await self._get_story_context_from_faiss_index(user_choice)

        # Get dynamic recent history (last 3 turns)
        recent_history = await self._get_history_text(3)

        prompt = (
            f"You are the Story Weaver for '{self.story_info['title']}'. "
            f"Follow Episode game rules: brief narration, personal choices, consequences matter.\n\n"
            f"=== STORY WORLD & LORE (Reference Only) ===\n"
            f"{story_folklore}\n\n"
            f"=== RECENT GAMEPLAY (Last 3 Turns) ===\n"
            f"{recent_history if recent_history else 'Story just started'}\n\n"
            f"=== PLAYER'S CURRENT CHOICE ===\n"
            f"{user_choice}\n\n"
            f"=== YOUR TASK ===\n"
            f"Continue the story based on the player's choice. "
            f"Use the lore for consistency, but prioritize recent events for continuity.\n"
            f"Generate:\n"
            f"1. Brief narration (150-250 words) of what happens\n"
            f"2. Exactly 3-4 personal, action-oriented choices\n\n"
            f"=== OUTPUT FORMAT (STRICT JSON) ===\n"
            f"""{{
  "narration": "Your engaging narration here...",
  "options": ["Choice 1", "Choice 2", "Choice 3"]
}}"""
        )
        return prompt


# agent = StoryRAGAgent("mystery_mansion")
# result = agent.generate_next("Go left into the forest")
# print(result)  # Example usage, should be removed in production code
