#!/usr/bin/env python3
"""
Test script to verify RAG retrieval is working correctly.

Usage:
    python scripts/test_rag.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from episode.logic.story_agent import StoryRAGAgent
from episode.story_registry import stories


async def test_rag_retrieval():
    """Test RAG retrieval with a sample query."""
    print("=" * 70)
    print("Testing RAG Retrieval System")
    print("=" * 70)

    # Test story
    story_id = "mystery_mansion"
    session_id = "test-session-123"

    print(f"\n📚 Story: {stories[story_id]['title']}")
    print(f"🔑 Session: {session_id}\n")

    # Create agent
    try:
        agent = StoryRAGAgent(story_id, session_id)
        print("✓ Agent initialized successfully\n")
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}")
        return

    # Test folklore retrieval
    test_choice = "Investigate the library for clues about Alistair's disappearance"

    print(f"🎮 Test User Choice: '{test_choice}'\n")
    print("-" * 70)
    print("Retrieving story folklore from vector DB...")
    print("-" * 70)

    try:
        # Get folklore context
        folklore = await agent._get_story_context_from_faiss_index(test_choice)

        print("\n📖 Retrieved Folklore Context:\n")
        print(folklore)
        print("\n" + "=" * 70)

        if folklore:
            print("✓ RAG retrieval working correctly!")
            print(f"  Retrieved {len(folklore)} characters of context")
        else:
            print("⚠ Warning: No folklore context retrieved")

    except Exception as e:
        print(f"\n✗ Error during retrieval: {e}")
        import traceback

        traceback.print_exc()


async def test_full_turn():
    """Test a complete story turn generation."""
    print("\n" + "=" * 70)
    print("Testing Full Story Turn Generation")
    print("=" * 70)

    story_id = "mystery_mansion"
    session_id = "test-session-456"

    agent = StoryRAGAgent(story_id, session_id)

    # Start the story
    test_choice = "Begin the investigation"

    print(f"\n🎮 User Choice: '{test_choice}'\n")
    print("Generating story turn...")
    print("-" * 70)

    try:
        result = await agent.generate_next(test_choice)

        print("\n📝 AI Response:\n")
        print(f"Narration: {result['response'].get('narration', 'N/A')}\n")
        print("Options:")
        for i, option in enumerate(result["response"].get("options", []), 1):
            print(f"  {i}. {option}")

        print("\n" + "=" * 70)
        print("✓ Full story turn generation successful!")

    except Exception as e:
        print(f"\n✗ Error during generation: {e}")
        import traceback

        traceback.print_exc()


async def main():
    """Run all tests."""
    await test_rag_retrieval()

    print("\n\n")

    # Uncomment to test full turn (requires GEMINI_API_KEY)
    # await test_full_turn()


if __name__ == "__main__":
    asyncio.run(main())
