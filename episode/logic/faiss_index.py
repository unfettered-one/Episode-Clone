from __future__ import annotations

import logging
from pathlib import Path
from asyncio import to_thread
from typing import Optional, List

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from episode.configuration import settings

LOGGER = logging.getLogger(__name__)


class FaissIndex:
    """
    FAISS-based vector index using Gemini embeddings.
    Lambda-safe (no local ML models).
    """

    def __init__(self) -> None:
        
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        self.story_docs_path: str = settings.story_docs_path()
        self.vector_db_path: str = settings.vector_db_path()

    async def create_faiss_index(self, story_id: str) -> None:
        """
        Create a FAISS index from base story documents.
        """
        all_docs: List[Document] = []

        common_story_id = story_id.split("-")[0]
        docs_path = Path(self.story_docs_path) / common_story_id

        if not docs_path.exists():
            LOGGER.warning("Story docs path does not exist: %s", docs_path)
            return

        for file in docs_path.glob("*.txt"):
            loader = TextLoader(str(file))
            docs = loader.load()
            all_docs.extend(docs)

        if not all_docs:
            LOGGER.warning("No documents found for story_id=%s", story_id)
            return

        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(all_docs)

        # FAISS creation (sync → run in thread)
        db = await to_thread(
            FAISS.from_documents,
            chunks,
            self.embedding_model,
        )

        save_path = Path(self.vector_db_path) / story_id
        db.save_local(str(save_path))

        LOGGER.info("FAISS index created at %s", save_path)

    async def add_to_faiss_index(self, story_id: str, text: str) -> None:
        """
        Add new text to an existing FAISS index.
        """
        path_to_story_db = Path(self.vector_db_path) / story_id

        if path_to_story_db.exists():
            db = FAISS.load_local(
                str(path_to_story_db),
                self.embedding_model,
                allow_dangerous_deserialization=True,
            )
        else:
            # Create empty index if missing
            db = FAISS.from_texts([], self.embedding_model)

        await to_thread(db.add_texts, [text])
        db.save_local(str(path_to_story_db))

    async def _query_faiss_index(self, story_id: str) -> FAISS:
        """
        Load or create FAISS index for a story.
        """
        path_to_story_db = Path(self.vector_db_path) / story_id

        if not path_to_story_db.exists():
            await self.create_faiss_index(story_id)

        return FAISS.load_local(
            str(path_to_story_db),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )

    async def similarity_search(
        self,
        query: str,
        story_id: str,
        top_chunks: Optional[int] = None,
    ) -> List[Document]:
        """
        Perform similarity search on FAISS index.
        """
        db = await self._query_faiss_index(story_id)

        search_kwargs = {}
        if top_chunks:
            search_kwargs["k"] = top_chunks

        retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs=search_kwargs,
        )

        # retriever.invoke is sync → move to thread
        return await to_thread(retriever.invoke, query)

    async def query_story_response(self, query: str, story_id: str) -> str:
        """
        Fetch relevant story context as plain text.
        """
        docs = await self.similarity_search(query, story_id, None)
        return "\n\n".join(doc.page_content for doc in docs)
