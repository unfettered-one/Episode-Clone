from story_registry import stories
from logic.fiass_index import FaissIndex
from logic.gemini_magic import gemini

import json


class StoryRAGAgent:
    def __init__(self, story_id: str):
        if story_id not in stories:
            raise ValueError(f"Unknown story ID: {story_id}")

        self.story_id = story_id
        self.story_info = stories[story_id]
        self.chat_history = []
        self.faiss_index = FaissIndex()

    async def generate_next(self, user_choice: str) -> dict:
        prompt = await self._generate_prompt_for_agent(user_choice)

        response = await gemini.generate_response(prompt)
        cleaned_response = await self._convert_ai_response_text_to_json(response)
        self.chat_history.append(user_choice)
        return {"response": cleaned_response}

    async def _convert_ai_response_text_to_json(self, ai_response: str) -> dict:
        # Convert the AI response text to JSON format
        cleaned = ai_response.strip().replace("```json", "").replace("```", "").strip()
        json_response = json.loads(cleaned)
        return json_response

    async def _get_last_n_choices(self, n: int) -> list[str]:
        max_choices = min(n, len(self.chat_history), 0)
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
        docs = await self.faiss_index.similarity_search(query, self.story_id)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    async def _common_query_to_ask_to_agent(self, user_choice: str) -> str:
        return f"Based on the story context and player's recent choice {user_choice}, continue the story , and pop 3 new choices in the next turn"

    async def _generate_prompt_for_agent(self, user_choice: str) -> str:

        history_text = await self._get_history_text(3)
        story_context = await self._get_story_context_from_faiss_index(user_choice)
        prompt = (
            f"Story Title: {self.story_info['title']}\n"
            f"Story Description: {self.story_info['description']}\n\n"
            f"User History:\n{history_text}\n\n"
            f"Relevant Story Context:\n{story_context}\n\n"
            f"User chose: {user_choice}\n"
            f"Generate next narration and options for the user.\n"
            f"you know the Episode game that is very popular, make sure that you are following its style for options\n"
            f"""Return the response strictly as JSON\n:
            {{
                "narration": "full narration text",
                "options": ["Option 1", "Option 2", "Option 3"]
            }}"""
        )
        return prompt


# agent = StoryRAGAgent("mystery_mansion")
# result = agent.generate_next("Go left into the forest")
# print(result)  # Example usage, should be removed in production code
