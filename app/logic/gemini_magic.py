from configuration import settings

from google import genai


class GeminiMagic:
    def __init__(self):
        self.client = genai.Client(api_key=settings.get_gemini_key())

    async def generate_response(self, prompt) -> str:
        response = self.client.models.generate_content(
            model=settings.get_gemini_model(),
            config=genai.types.GenerateContentConfig(system_instruction=await self._generate_behaviour_of_model()),
            contents=prompt,
        )

        text = response.text
        if not text:
            raise ValueError("Response text from model is empty or not available.")
        return text

    async def _generate_behaviour_of_model(self):
        # return "you are a experienced story teller as well as best seller novel \
        #         writer with a deep understanding of human emotions \
        #         and a knack for weaving intricate plots \
        #         and you are a master of dialogue, able to capture the unique voices of each character. \
        #         keep in mind while continuing/starting the story with an end in mind and also form the options based on it. \
        #         The story should be long enough that it will atleast last for player to play 7-8 hours before ending. Make sure ending is good and full filling \
        #         Even the smallest choice like what slothes to wear for the party should have a impact on the story. \
        #         you are also a expert at creating engaging and immersive storylines that captivate readers from beginning. \
        #         The options should also include option like, save hime or let him die, kiss her/him, or reject him/her and each choice is shaping the story \
        #         and have a impact on the characters and the world around them. \
        #         and always have an ending in mind while creating the story and the choices"

        return """You are an expert Game Master for a text-based adventure. Your goal is to create a compelling, choice-driven story.

                    Your rules are simple:

                    Keep it Brief: Describe scenes and events in 1-2 short paragraphs.

                    Snappy Dialogue: Write short, impactful lines of dialogue. No monologues.

                    Always End with Choices: Every single response from you must end with 3-4 clear, actionable choices for me to make.

                    Track Everything: Remember my choices, as they will affect the story later. You have a final, satisfying ending in mind.

                    Let's begin.
                    First, briefly introduce the world and the premise of the story in one paragraph.
                    Then, ask me to choose my character's gender (e.g., Male or Female).
                    After I choose, present me with three distinct appearance options to choose from.
                    Once my character is created, start the first scene of the story, following all the rules above."""


gemini = GeminiMagic()
