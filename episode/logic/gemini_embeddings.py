"""
Custom Embeddings class using Google's genai SDK.
Compatible with LangChain's Embeddings interface for use with FAISS.
"""

from __future__ import annotations

import logging
from typing import List

from google import genai
from langchain_core.embeddings import Embeddings

LOGGER = logging.getLogger(__name__)


class GeminiEmbeddings(Embeddings):
    """
    Custom embeddings class using Google's genai SDK directly.

    This replaces the deprecated langchain_google_genai.GoogleGenerativeAIEmbeddings
    by using the google-genai library's embed_content method directly.
    """

    def __init__(self, api_key: str, model: str = "gemini-embedding-001"):
        """
        Initialize Gemini embeddings.

        Args:
            api_key: Google AI API key
            model: Embedding model name (default: gemini-embedding-001)
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please set the GEMINI_API_KEY environment variable.")
        self.client = genai.Client(api_key=api_key)
        self.model = model
        LOGGER.info(f"Initialized GeminiEmbeddings with model: {model}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        embeddings = []
        # Process in batches to avoid rate limits (max 100 per request)
        batch_size = 100

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            try:
                result = self.client.models.embed_content(
                    model=self.model,
                    contents=batch,
                )

                # Extract embeddings from response
                if result.embeddings:
                    for embedding in result.embeddings:
                        embeddings.append(embedding.values)

            except Exception as e:
                LOGGER.error(f"Error embedding batch {i // batch_size}: {e}")
                raise

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.

        Args:
            text: Query string to embed

        Returns:
            Embedding vector
        """
        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=[text],
            )
            if result.embeddings and result.embeddings[0].values:
                return result.embeddings[0].values
            else:
                raise ValueError("No embeddings returned from API")

        except Exception as e:
            LOGGER.error(f"Error embedding query: {e}")
            raise
