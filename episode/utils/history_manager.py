"""
History Manager - DynamoDB-backed story session management.
Replaces file-based text_manager with proper database storage.
"""

import logging
from datetime import datetime, timezone

from episode.aws_proxy.utils import get_dynamodb_operations
from episode.configuration import settings

LOGGER = logging.getLogger(__name__)


class HistoryManager:
    """
    Manages story turn history using DynamoDB.
    Designed for Lambda environment - stateless and scalable.

    DynamoDB Schema:
    - PK: pk (partition key) - session_id (story_id-user_id) - String
    - SK: sk (sort key) - turn_number as string - String
    - Attributes: user_choice, narration, options, timestamp

    Special item: sk="0" stores metadata (current_turn count)
    """

    def __init__(self):
        """Initialize DynamoDB operations client."""
        self.table_name = settings.get_dynamodb_table_name()
        self.region = settings.get_aws_region()
        self.db_ops = get_dynamodb_operations(table_name=self.table_name, region_name=self.region)
        LOGGER.info(f"HistoryManager initialized with table: {self.table_name}, region: {self.region}")

    async def save_turn(self, session_id: str, turn_number: int, user_choice: str, ai_response: dict) -> None:
        """
        Save a story turn to DynamoDB.

        Args:
            session_id: Unique session identifier (story_id-user_id)
            turn_number: Sequential turn number
            user_choice: What the player chose
            ai_response: AI's response with narration and options
        """
        item = {
            "pk": session_id,  # Generic partition key
            "sk": str(turn_number),  # Generic sort key (string)
            "user_choice": user_choice,
            "narration": ai_response.get("narration", ""),
            "options": ai_response.get("options", []),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        try:
            self.db_ops.create_item(item)
            LOGGER.info(f"Turn {turn_number} saved for session: {session_id}")
        except Exception as e:
            LOGGER.error(f"Failed to save turn: {e}")
            raise

    async def get_last_n_turns(self, session_id: str, n: int) -> list[dict]:
        """
        Retrieve last N turns for a session.

        Args:
            session_id: Session identifier
            n: Number of recent turns to retrieve

        Returns:
            List of turn dicts with 'choice' and 'narration'
        """
        # In production, use Query with ScanIndexForward=False and Limit=n
        # For now, we'll use a simple approach

        turns = []
        try:
            # Get the current turn count first
            turn_count = await self.get_turn_count(session_id)

            if turn_count == 0:
                return []

            # Calculate starting turn number
            start_turn = max(1, turn_count - n + 1)

            # Fetch each turn
            for turn_num in range(start_turn, turn_count + 1):
                turn_data = self.db_ops.get_item({"pk": session_id, "sk": str(turn_num)})

                if turn_data:
                    turns.append(
                        {"choice": turn_data.get("user_choice", ""), "narration": turn_data.get("narration", "")}
                    )

            LOGGER.info(f"Retrieved {len(turns)} turns for session: {session_id}")
            return turns

        except Exception as e:
            LOGGER.error(f"Failed to retrieve turns: {e}")
            return []

    async def get_turn_count(self, session_id: str) -> int:
        """
        Get the current turn count for a session.
        Uses a metadata item to track count.

        Args:
            session_id: Session identifier

        Returns:
            Current turn number
        """
        try:
            metadata = self.db_ops.get_item({"pk": session_id, "sk": "0"})  # sk="0" stores metadata

            if metadata:
                return metadata.get("current_turn", 0)
            return 0

        except Exception as e:
            LOGGER.warning(f"Failed to get turn count, defaulting to 0: {e}")
            return 0

    async def increment_turn_count(self, session_id: str) -> int:
        """
        Increment and return the turn count for a session.

        Args:
            session_id: Session identifier

        Returns:
            New turn number
        """
        try:
            # Try to get current count
            current_count = await self.get_turn_count(session_id)
            new_count = current_count + 1

            # Update metadata
            if current_count == 0:
                # Create metadata item
                self.db_ops.create_item(
                    {
                        "pk": session_id,
                        "sk": "0",
                        "current_turn": new_count,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
            else:
                # Update existing metadata
                self.db_ops.update_item(
                    key={"pk": session_id, "sk": "0"},
                    update_expression="SET current_turn = :count",
                    expression_values={":count": new_count},
                )

            return new_count

        except Exception as e:
            LOGGER.error(f"Failed to increment turn count: {e}")
            raise

    async def delete_session(self, session_id: str) -> None:
        """
        Delete all turns for a session.

        Args:
            session_id: Session identifier to delete
        """
        try:
            turn_count = await self.get_turn_count(session_id)

            # Delete all turns including metadata (turn 0)
            for turn_num in range(0, turn_count + 1):
                self.db_ops.delete_item({"pk": session_id, "sk": str(turn_num)})

            LOGGER.info(f"Deleted session: {session_id}")

        except Exception as e:
            LOGGER.error(f"Failed to delete session: {e}")
            raise

    async def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: Session identifier

        Returns:
            True if session has any turns
        """
        try:
            turn_count = await self.get_turn_count(session_id)
            return turn_count > 0
        except:
            return False


# Singleton instance
history_manager = HistoryManager()
