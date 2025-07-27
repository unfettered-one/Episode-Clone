from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv(dotenv_path="./.local/.env")


def create_faiss_index(story_id: str, docs_path: str, save_path: str):
    all_docs = []
    docs_path = docs_path + f"/{story_id}"
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    for file in Path(docs_path).glob("*.txt"):
        loader = TextLoader(str(file))
        docs = loader.load()
        all_docs.extend(docs)

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)

    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(save_path)
    print(f"Vector DB saved to {save_path}")


# Example usage
if __name__ == "__main__":
    create_faiss_index(
        story_id="mystery_mansion", docs_path="./app/story_docs", save_path="./vector_db/mystery_mansion"
    )
