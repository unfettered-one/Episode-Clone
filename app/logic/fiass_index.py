from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.text_splitter import CharacterTextSplitter
from google import genai


from pathlib import Path

from langchain.schema import Document

from configuration import settings

import logging
import asyncio


LOGGER = logging.getLogger(__name__)


class FaissIndex:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_key())
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        self.story_docs_path = settings.story_docs_path()
        self.vector_db_path = settings.vector_db_path()

    def create_faiss_index(self, story_id: str):
        all_docs = []
        docs_path = self.story_docs_path + f"/{story_id}"

        for file in Path(docs_path).glob("*.txt"):
            loader = TextLoader(str(file))
            docs = loader.load()
            all_docs.extend(docs)

        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(all_docs)

        db = FAISS.from_documents(chunks, self.embedding_model)
        db.save_local(self.vector_db_path + f"/{story_id}")
        print(f"Vector DB saved to {self.vector_db_path + f'/{story_id}'}")

    def query_faiss_index(self, query: str, story_id: str, k: int = 5) -> FAISS:
        """
        Searches the FAISS index for the most relevant documents given a user query.
        """
        db = FAISS.load_local(
            self.vector_db_path + f"/{story_id}", embeddings=self.embedding_model, allow_dangerous_deserialization=True
        )
        return db

    def similarity_search(self, query: str, story_id: str, k: int = 5) -> list[Document]:
        """
        Performs a similarity search on the FAISS index.
        """
        db = self.query_faiss_index(query, story_id, k)
        return db.similarity_search(query, k=k)

    def query_story_response(self, query: str, story_id: str):
        db = self.query_faiss_index(query, story_id)
        retriever = db.as_retriever()

        # Retrieve relevant documents
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in docs])


        prompt = (
            f"Based on the following story context, answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Answer:"
        )

        try:
            response = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            return response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            LOGGER.error("Error during Gemini query: %s", e)
            return str(e)


# x = FaissIndex()
# y = x.query_story_response(story_id="mystery_mansion", query="Summarize the story.")
# print(y)
