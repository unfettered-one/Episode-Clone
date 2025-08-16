from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

# from google import genai


from pathlib import Path
from configuration import settings
import logging


LOGGER = logging.getLogger(__name__)


class FaissIndex:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        self.story_docs_path = settings.story_docs_path()
        self.vector_db_path = settings.vector_db_path()

    async def create_faiss_index(self, story_id: str):
        all_docs = []
        common_story_id = story_id.split("-")[0]
        docs_path = self.story_docs_path + f"/{common_story_id}"

        for file in Path(docs_path).glob("*.txt"):
            loader = TextLoader(str(file))
            docs = loader.load()
            all_docs.extend(docs)

        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(all_docs)

        db = FAISS.from_documents(chunks, self.embedding_model)
        db.save_local(self.vector_db_path + f"/{story_id}")
        print(f"Vector DB saved to {self.vector_db_path + f'/{story_id}'}")

    async def add_to_faiss_index(self, story_id: str, text: str) -> None:
        path_to_story_db = self.vector_db_path + f"/{story_id}"

        # Load existing index
        if Path(path_to_story_db).exists():
            db = FAISS.load_local(path_to_story_db, self.embedding_model, allow_dangerous_deserialization=True)
        else:
            db = FAISS.from_texts([], self.embedding_model)

        # Add new chunk
        db.add_texts([text])

        # Save updated index
        db.save_local(path_to_story_db)

    async def _query_faiss_index(
        self,
        story_id: str,
    ) -> FAISS:
        """
        Searches the FAISS index for the most relevant documents given a user query.
        """
        path_to_story_db = self.vector_db_path + f"/{story_id}"

        if not Path(path_to_story_db).exists():

            await self.create_faiss_index(story_id)
        db = FAISS.load_local(path_to_story_db, embeddings=self.embedding_model, allow_dangerous_deserialization=True)
        return db

    async def similarity_search(self, query: str, story_id: str, top_chunks: int | None) -> list[Document]:
        """
        Performs a similarity search on the FAISS index.
        """
        db = await self._query_faiss_index(
            story_id=story_id,
        )
        params_for_search = {}
        if top_chunks:
            params_for_search["k"] = top_chunks
        retriever = db.as_retriever(search_type="similarity", search_kwargs=params_for_search)
        return retriever.invoke(query)

    async def query_story_response(self, query: str, story_id: str):
        # Retrieve relevant documents
        docs = await self.similarity_search(query, story_id, None)
        context = "\n\n".join([doc.page_content for doc in docs])

        # prompt = (
        #     f"Based on the following story context, answer the question.\n\n"
        #     f"Context:\n{context}\n\n"
        #     f"Question: {query}\n\n"
        #     f"Answer:"
        # )

        # try:
        #     response = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        #     return response.text if hasattr(response, "text") else str(response)
        # except Exception as e:
        #     LOGGER.error("Error during Gemini query: %s", e)
        #     return str(e)


# x = FaissIndex()
# # y = x.similarity_search(story_id="mystery_mansion", query="Summarize the story.")
# y = asyncio.run(x.query_story_response(story_id="mystery_mansion", query="Summarize the story."))
# print(y)
