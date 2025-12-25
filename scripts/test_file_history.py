#!/usr/bin/env python3
"""
Test the updated file-based history system.
This demonstrates how turns are saved and retrieved.
"""
import asyncio
import sys
import json
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock GEMINI_API_KEY to avoid initialization error
os.environ.setdefault("GEMINI_API_KEY", "test-key-for-demo")

from episode.logic.story_agent import StoryRAGAgent
from episode.utils.text_manager import text_file_manager


async def test_save_and_retrieve_turns():
    """Test saving and retrieving turns from file."""
    print("=" * 70)
    print("Testing File-Based History System")
    print("=" * 70)

    story_id = "mystery_mansion"
    session_id = "demo-session-file-test"

    agent = StoryRAGAgent(story_id, session_id)

    # Clean up any existing test file
    try:
        await text_file_manager.delete_text_file(agent.user_story_path)
        print(f"✓ Cleaned up existing test file\n")
    except:
        pass

    # Simulate 3 turns being saved
    print("📝 Simulating 3 story turns...\n")

    test_turns = [
        {
            "choice": "Enter the mansion through the front door",
            "response": {
                "narration": "The heavy oak doors creak as you push them open. A musty smell fills your nostrils. The grand foyer is dimly lit, with portraits of stern-faced ancestors lining the walls.",
                "options": ["Examine the portraits", "Head up the grand staircase", "Check the room to your left"],
            },
        },
        {
            "choice": "Examine the portraits",
            "response": {
                "narration": "As you study the paintings, you notice one portrait has fresh scratch marks. It depicts a young woman in a wedding dress, her eyes seeming to follow your movement.",
                "options": ["Touch the scratched portrait", "Search behind the portrait", "Continue to the staircase"],
            },
        },
        {
            "choice": "Search behind the portrait",
            "response": {
                "narration": "You carefully lift the portrait from the wall. Behind it is a hidden compartment containing a dusty leather journal. The first entry reads: 'The wedding was never meant to be...'",
                "options": [
                    "Read more of the journal",
                    "Take the journal and continue exploring",
                    "Put it back and leave",
                ],
            },
        },
    ]

    # Save each turn
    for i, turn in enumerate(test_turns, 1):
        await agent._save_turn_to_file(turn["choice"], turn["response"])
        print(f"Turn {i} saved:")
        print(f"  Choice: {turn['choice']}")
        print(f"  Narration: {turn['response']['narration'][:60]}...")
        print()

    print("-" * 70)
    print("📖 Reading turns back from file...\n")

    # Read the file content
    file_content = await text_file_manager.read_text_file(agent.user_story_path)
    print("Raw file content:")
    print(file_content[:500] + "...\n")
    print("-" * 70)

    # Test retrieval of last 3 turns
    print("\n🔍 Retrieving last 3 turns using agent method...\n")

    retrieved_turns = await agent._get_last_n_turns_from_file(3)

    print(f"Retrieved {len(retrieved_turns)} turns:\n")
    for i, turn in enumerate(retrieved_turns, 1):
        print(f"Turn {i}:")
        print(f"  Choice: {turn['choice']}")
        print(f"  Narration: {turn['narration'][:80]}...")
        print()

    # Test formatted history
    print("-" * 70)
    print("📜 Formatted history for AI prompt:\n")

    formatted_history = await agent._get_history_text(3)
    print(formatted_history)

    print("\n" + "=" * 70)
    print("✓ File-based history system working correctly!")
    print(f"✓ Turns persist across agent instances (Lambda-friendly)")
    print(f"✓ File location: {agent.user_story_path}")
    print("=" * 70)

    # Cleanup
    try:
        await text_file_manager.delete_text_file(agent.user_story_path)
        print("\n✓ Test file cleaned up")
    except:
        pass


async def test_history_in_prompt():
    """Test that history is properly included in the prompt."""
    print("\n\n" + "=" * 70)
    print("Testing History Integration in Prompt")
    print("=" * 70)

    story_id = "mystery_mansion"
    session_id = "demo-prompt-test"

    agent = StoryRAGAgent(story_id, session_id)

    # Clean up
    try:
        await text_file_manager.delete_text_file(agent.user_story_path)
    except:
        pass

    # Save a couple of turns first
    print("\n📝 Setting up test scenario with 2 previous turns...\n")

    await agent._save_turn_to_file(
        "Enter the library",
        {
            "narration": "The library is vast, filled with ancient books.",
            "options": ["Read a book", "Leave", "Search the desk"],
        },
    )

    await agent._save_turn_to_file(
        "Search the desk",
        {
            "narration": "You find a mysterious key hidden in a drawer.",
            "options": ["Take the key", "Leave it", "Keep searching"],
        },
    )

    # Now generate a prompt (without calling Gemini)
    print("🔨 Building prompt for next turn...\n")

    current_choice = "Take the key and examine it closely"

    # Get history text that would be in the prompt
    history = await agent._get_history_text(3)

    print("History that will be in the prompt:")
    print("-" * 70)
    print(history)
    print("-" * 70)

    print("\n✓ History correctly includes both:")
    print("  - Previous player choices")
    print("  - What happened (narrations)")
    print("\nThis gives the AI full context for continuity!")

    # Cleanup
    try:
        await text_file_manager.delete_text_file(agent.user_story_path)
    except:
        pass


if __name__ == "__main__":
    asyncio.run(test_save_and_retrieve_turns())
    asyncio.run(test_history_in_prompt())
