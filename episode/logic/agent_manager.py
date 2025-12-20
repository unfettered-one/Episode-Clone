from episode.logic.story_agent import StoryRAGAgent
import logging

LOGGER = logging.getLogger(__name__)


class AgentManager:
    _instance = None
    _agents: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
            cls._instance._agents = {}
        return cls._instance

    async def get_agent(self, story_id: str, session_id: str) -> StoryRAGAgent:
        key = f"{story_id}-{session_id}"
        LOGGER.info("Retrieving agent for story_id: %s, session_id: %s, key: %s", story_id, session_id, key)
        if key not in self._agents:
            self._agents[key] = StoryRAGAgent(story_id, session_id)

        return self._agents[key]
