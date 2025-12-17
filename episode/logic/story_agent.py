import json
import logging

from logic.faiss_index import FaissIndex
from logic.gemini_magic import gemini

from utils.text_manager import text_file_manager
from story_registry import stories
from configuration import settings

LOGGER = logging.getLogger(__name__)


class StoryRAGAgent:
    def __init__(self, story_id: str, session_id: str):
        if story_id not in stories:
            raise ValueError(f"Unknown story ID: {story_id}")

        self.story_id = story_id
        self.story_info = stories[story_id]
        self.chat_history = []
        self.faiss_index = FaissIndex()
        self.common_story_path = f"{settings.story_docs_path()}/{self.story_id}.txt"
        self.session_id = session_id
        self.user_story_id = self.story_id + "-" + self.session_id
        self.user_story_path = f"{settings.story_docs_path()}/{self.user_story_id}.txt"

    async def generate_next(self, user_choice: str) -> dict:
        prompt = await self._generate_prompt_for_agent(user_choice)

        response = await gemini.generate_response(prompt)
        cleaned_response = await self._convert_ai_response_text_to_json(response)
        await self._update_story(self.user_story_id, response)
        return {"response": cleaned_response}

    async def _convert_ai_response_text_to_json(self, ai_response: str) -> dict:
        # Convert the AI response text to JSON format
        cleaned = ai_response.strip().replace("```json", "").replace("```", "").strip()
        json_response = json.loads(cleaned)
        return json_response

    async def _get_last_n_choices(self, n: int) -> list[str]:
        max_choices = max(min(n, len(self.chat_history)), 0)
        if max_choices > 0:
            return self.chat_history[-max_choices:]
        return []

    async def _convert_choices_to_history_text(self, choices: list[str]) -> str:
        return "\n".join(f"Choice :- {choice}" for choice in choices)

    async def _get_history_text(self, last_recent_choices: int) -> str:
        last_n_chats = await self._get_last_n_choices(last_recent_choices)
        return await self._convert_choices_to_history_text(last_n_chats)

    async def _get_story_context_from_faiss_index(self, user_choice: str) -> str:
        query = await self._common_query_to_ask_to_agent(user_choice)
        docs = await self.faiss_index.similarity_search(query, self.user_story_id, None)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    async def _common_query_to_ask_to_agent(self, user_choice: str) -> str:
        return f"Based on the story context and player's recent choice {user_choice}, continue the story , and pop 3 new choices in the next turn"

    async def _generate_prompt_for_agent(self, user_choice: str) -> str:

        history_text = await self._get_history_text(3)
        story_context = await self._get_story_context_from_faiss_index(user_choice)
        name = "Yash"
        prompt = (
            f"You are the Story Weaver. Remember your core principles: brief narration, 'Episode' style choices, and consequences. "
            f"The story is '{self.story_info['title']}'.\n\n"
            f"Recent History (Last 3 turns):\n{history_text}\n\n"
            f"Current Situation & World Context:\n{story_context}\n\n"
            f"In the last turn, I chose to: '{user_choice}'\n\n"
            f"Based on my choice, continue the story. Generate a concise narration for the outcome and provide the next set of 3-4 personal, action-oriented choices.\n"
            f"Output must be a single, valid JSON object and nothing else."
            # This explicit structure reminder is highly effective.
            f"""Return the response strictly as JSON\n:
                "narration": "Your brief and engaging narration of what happens next...",
            {{
                "options": ["Option 1", "Option 2", "Option 3"]
            }}"""
        )
        return prompt

    async def _update_story(self, session_id: str, content: str):
        """Update the user's story file with new content."""

        await text_file_manager.append_text_file(content, self.user_story_path)
        try:
            await self.faiss_index.add_to_faiss_index(session_id, content)
        except Exception as e:
            LOGGER.error("Error updating FAISS index: %s", e)


# agent = StoryRAGAgent("mystery_mansion")
# result = agent.generate_next("Go left into the forest")
# print(result)  # Example usage, should be removed in production code
