from story_registry import stories


class StoryRAGAgent:
    def __init__(self, story_id: str):
        if story_id not in stories:
            raise ValueError(f"Unknown story ID: {story_id}")

        self.story_id = story_id
        self.story_info = stories[story_id]
        self.chat_history = []

    async def generate_next(self, user_choice: str | None = None) -> dict:
        # For now, Static response generation
        # In a real implementation, this would involve more complex logic
        dummy_narration = (
            f"You are in the story: {self.story_info['title']}. You chose: {user_choice or 'nothing yet'}."
        )
        dummy_choices = ["Go left into the forest", "Climb the old tower", "Ask the stranger for help"]

        self.chat_history.append((user_choice, dummy_narration))
        return {"narration": dummy_narration, "choices": dummy_choices}


# agent = StoryRAGAgent("mystery_mansion")
# result = agent.generate_next("Go left into the forest")
# print(result)  # Example usage, should be removed in production code
