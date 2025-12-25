from pathlib import Path
import logging

LOGGER = logging.getLogger(__name__)


class TextFileManager:
    def __init__(self):
        """
        Helper class to manage text files
        """
        pass

    async def append_text_file(self, content: str, path: str):
        """Append content to the user's text file."""
        file_path = Path(path)
        if not await self._check_if_file_exists(file_path):
            LOGGER.info("File does not exist, creating new file %s", path)
            await self.create_text_file(content, path)
            return

        try:
            with file_path.open("a", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            raise RuntimeError(f"Error appending to text file: {e}")

    async def read_text_file(self, path: str) -> str:
        """
        Read entire text file content.
        Useful for retrieving story progression history.
        """
        file_path = Path(path)
        if not await self._check_if_file_exists(file_path):
            LOGGER.warning("File does not exist: %s", path)
            return ""

        try:
            with file_path.open("r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(f"Error reading text file: {e}")

    async def get_last_n_entries(self, path: str, n: int, separator: str = "\n\n") -> list[str]:
        """
        Get last N entries from a text file.
        Useful for retrieving recent story turns.

        Args:
            path: Path to text file
            n: Number of entries to retrieve
            separator: String that separates entries (default: double newline)

        Returns:
            List of last N entries
        """
        content = await self.read_text_file(path)
        if not content:
            return []

        entries = content.split(separator)
        # Filter out empty entries
        entries = [e.strip() for e in entries if e.strip()]
        return entries[-n:] if len(entries) >= n else entries

    async def _check_if_file_exists(self, path: Path) -> bool:
        """Check if a file exists."""
        return path.is_file()

    async def create_text_file(self, content: str, path: str):
        """Create a new text file with the given content."""
        file_path = Path(path)
        if await self._check_if_file_exists(file_path):
            raise FileExistsError("File already exists.")

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)  # ensure directory exists
            with file_path.open("w", encoding="utf-8") as file:
                file.write(content)
            LOGGER.info("Text file created at %s", path)
        except Exception as e:
            raise RuntimeError(f"Error creating text file: {e}")

    async def delete_text_file(self, path: str):
        """Delete the user's text file."""
        file_path = Path(path)
        if not await self._check_if_file_exists(file_path):
            raise FileNotFoundError("User story file does not exist.")

        try:
            file_path.unlink()
        except Exception as e:
            raise RuntimeError(f"Error deleting text file: {e}")


text_file_manager = TextFileManager()
