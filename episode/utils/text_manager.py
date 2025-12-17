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
