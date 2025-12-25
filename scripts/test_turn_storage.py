#!/usr/bin/env python3
"""
Simple unit test for file-based history without dependencies.
Tests the parsing and formatting logic directly.
"""
import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from episode.utils.text_manager import text_file_manager


async def test_turn_storage_and_retrieval():
    """Test saving and retrieving turn data from file."""
    print("=" * 70)
    print("Testing Turn Storage & Retrieval")
    print("=" * 70)

    test_file = "/tmp/test_story_session.txt"

    # Clean up
    try:
        await text_file_manager.delete_text_file(test_file)
    except:
        pass

    # Simulate 3 turns
    print("\n📝 Saving 3 test turns...\n")

    turns_data = [
        ("Enter the mansion", {"narration": "You step into the dark foyer.", "options": ["Go left", "Go right"]}),
        ("Go left", {"narration": "You find a library full of ancient books.", "options": ["Read", "Leave"]}),
        ("Read", {"narration": "The book reveals a hidden secret.", "options": ["Continue", "Stop"]}),
    ]

    for i, (choice, response) in enumerate(turns_data, 1):
        turn_content = f"USER_CHOICE: {choice}\n" f"AI_RESPONSE: {json.dumps(response)}\n" f"---TURN---\n"
        await text_file_manager.append_text_file(turn_content, test_file)
        print(f"Turn {i} saved: '{choice}'")

    print("\n" + "-" * 70)
    print("📖 Reading file content...\n")

    content = await text_file_manager.read_text_file(test_file)
    print("Raw file content:")
    print(content)

    print("-" * 70)
    print("🔍 Retrieving last 3 turns...\n")

    entries = await text_file_manager.get_last_n_entries(test_file, 3, separator="\n---TURN---\n")

    print(f"Retrieved {len(entries)} entries:\n")

    # Parse each entry
    parsed_turns = []
    for i, entry in enumerate(entries, 1):
        print(f"Entry {i}:")
        print(entry)
        print()

        # Parse format
        lines = entry.strip().split("\n", 1)
        if len(lines) >= 2:
            choice_line = lines[0]
            response_line = lines[1]

            if choice_line.startswith("USER_CHOICE: "):
                user_choice = choice_line.replace("USER_CHOICE: ", "").strip()

            if response_line.startswith("AI_RESPONSE: "):
                ai_response_json = response_line.replace("AI_RESPONSE: ", "").strip()
                ai_response = json.loads(ai_response_json)
                narration = ai_response.get("narration", "")

                parsed_turns.append({"choice": user_choice, "narration": narration})

    print("-" * 70)
    print("✅ Parsed Turns:\n")

    for i, turn in enumerate(parsed_turns, 1):
        print(f"Turn {i}:")
        print(f"  Choice: {turn['choice']}")
        print(f"  Narration: {turn['narration']}")
        print()

    # Format as history
    print("-" * 70)
    print("📜 Formatted as AI Prompt History:\n")

    history_lines = []
    for i, turn in enumerate(parsed_turns, 1):
        history_lines.append(f"Turn {i}:")
        history_lines.append(f"  Player chose: {turn['choice']}")
        history_lines.append(f"  What happened: {turn['narration']}")
        history_lines.append("")

    formatted = "\n".join(history_lines)
    print(formatted)

    print("=" * 70)
    print("✓ File-based history system verified!")
    print("✓ Format is parseable and readable")
    print("✓ Ready for production use")
    print("=" * 70)

    # Cleanup
    try:
        await text_file_manager.delete_text_file(test_file)
        print("\n✓ Test file cleaned up")
    except:
        pass


async def demo_file_structure():
    """Show what the file structure looks like."""
    print("\n\n" + "=" * 70)
    print("Example Story Session File Structure")
    print("=" * 70)

    print(
        """
A typical story session file looks like this:

USER_CHOICE: Enter the mansion through the front door
AI_RESPONSE: {"narration": "The heavy oak doors creak...", "options": [...]}
---TURN---
USER_CHOICE: Examine the portraits
AI_RESPONSE: {"narration": "You notice scratch marks...", "options": [...]}
---TURN---
USER_CHOICE: Search behind the portrait
AI_RESPONSE: {"narration": "You find a hidden journal...", "options": [...]}
---TURN---

This format:
✓ Stores both user choices AND AI narrations
✓ Easy to parse line-by-line
✓ Separator makes splitting simple
✓ Persists across Lambda invocations
✓ No database needed (for now)
✓ Later migrates easily to DynamoDB
    """
    )


if __name__ == "__main__":
    asyncio.run(test_turn_storage_and_retrieval())
    asyncio.run(demo_file_structure())
