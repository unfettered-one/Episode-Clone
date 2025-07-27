from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from configuration import settings


class FaissIndex:
    def __init__(self):
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

    def query_faiss_index(self, query: str, story_id: str, k: int = 5) -> list[Document]:
        """
        Searches the FAISS index for the most relevant documents given a user query.
        """
        db = FAISS.load_local(
            self.vector_db_path + f"/{story_id}", embeddings=self.embedding_model, allow_dangerous_deserialization=True
        )
        results = db.similarity_search(query, k=k)
        return results


x = FaissIndex()
x.create_faiss_index("mystery_mansion")
