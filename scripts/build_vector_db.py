#!/usr/bin/env python3
"""
Script to build static FAISS vector databases for all stories.
Run this locally before deployment.

Usage:
    python scripts/build_vector_db.py
    python scripts/build_vector_db.py --story mystery_mansion
    python scripts/build_vector_db.py --delay 2  # Add 2s delay between stories
"""
import asyncio
import argparse
import logging
import time
from pathlib import Path

# Add parent directory to path for imports
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from episode.logic.faiss_index import FaissIndex
from episode.story_registry import stories
from episode.configuration import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)


async def build_vector_db_for_story(story_id: str, retry_on_quota: bool = False) -> None:
    """
    Build FAISS vector database for a single story.

    Args:
        story_id: Story identifier (e.g., 'mystery_mansion')
    """
    LOGGER.info("=" * 60)
    LOGGER.info(f"Building vector DB for story: {story_id}")
    LOGGER.info("=" * 60)

    # Verify story exists
    if story_id not in stories:
        LOGGER.error(f"Story '{story_id}' not found in registry!")
        LOGGER.error(f"Available stories: {list(stories.keys())}")
        return

    # Check if story docs exist
    story_docs_path = Path(settings.story_docs_path()) / story_id
    if not story_docs_path.exists():
        LOGGER.error(f"Story docs path does not exist: {story_docs_path}")
        return

    # Count text files
    txt_files = list(story_docs_path.glob("*.txt"))
    if not txt_files:
        LOGGER.warning(f"No .txt files found in {story_docs_path}")
        return

    LOGGER.info(f"Found {len(txt_files)} document(s):")
    for txt_file in txt_files:
        file_size = txt_file.stat().st_size
        LOGGER.info(f"  - {txt_file.name} ({file_size} bytes)")

    # Create vector DB
    max_retries = 3 if retry_on_quota else 1
    retry_count = 0

    while retry_count < max_retries:
        try:
            faiss_index = FaissIndex()
            await faiss_index.create_faiss_index(story_id)

            # Verify creation
            vector_db_path = Path(settings.vector_db_path()) / story_id
            if vector_db_path.exists():
                LOGGER.info(f"✓ Vector DB created successfully at: {vector_db_path}")

                # List created files
                db_files = list(vector_db_path.glob("*"))
                LOGGER.info(f"  Files created: {[f.name for f in db_files]}")
                break  # Success!
            else:
                LOGGER.error("✗ Vector DB creation failed - directory not found")
                break

        except Exception as e:
            error_msg = str(e)

            # Check if it's a quota error
            if "429" in error_msg or "quota" in error_msg.lower():
                retry_count += 1
                if retry_count < max_retries:
                    # Exponential backoff: 10s, 30s, 90s
                    wait_time = 10 * (3 ** (retry_count - 1))
                    LOGGER.warning(
                        f"⚠ Quota exceeded (attempt {retry_count}/{max_retries}). " f"Retrying in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    LOGGER.error(f"✗ Failed after {max_retries} attempts due to quota limits")
                    LOGGER.error(f"  Error: {e}")
                    raise
            else:
                # Non-quota error - fail immediately
                LOGGER.error(f"✗ Error building vector DB: {e}", exc_info=True)
                raise


async def build_all_vector_dbs(delay_between_stories: float = 0) -> None:
    """
    Build vector databases for all stories in registry.

    Args:
        delay_between_stories: Seconds to wait between stories to avoid rate limits
    """
    LOGGER.info("Building vector DBs for ALL stories...")
    LOGGER.info(f"Stories to process: {list(stories.keys())}\n")

    if delay_between_stories > 0:
        LOGGER.info(f"⏱️  Adding {delay_between_stories}s delay between stories\n")

    for i, story_id in enumerate(stories.keys()):
        try:
            await build_vector_db_for_story(story_id, retry_on_quota=True)
            LOGGER.info("")  # Blank line between stories

            # Add delay between stories if specified
            if delay_between_stories > 0 and i < len(stories) - 1:
                LOGGER.info(f"⏸️  Waiting {delay_between_stories}s before next story...")
                await asyncio.sleep(delay_between_stories)
                LOGGER.info("")

        except Exception as e:
            LOGGER.error(f"Failed to build vector DB for {story_id}: {e}")
            continue

    LOGGER.info("=" * 60)
    LOGGER.info("✓ All vector DBs built successfully!")
    LOGGER.info(f"Vector DB location: {settings.vector_db_path()}")
    LOGGER.info("=" * 60)


def main():
    """Main entry point for script."""
    parser = argparse.ArgumentParser(description="Build static FAISS vector databases for stories")
    parser.add_argument("--story", type=str, help="Specific story ID to build (default: build all)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run async build
    if args.story:
        asyncio.run(build_vector_db_for_story(args.story))
    else:
        asyncio.run(build_all_vector_dbs())


if __name__ == "__main__":
    main()
