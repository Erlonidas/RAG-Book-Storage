from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from typing import List, Dict
import os
from dotenv import load_dotenv
from src.config import setup_logger

logger = setup_logger(__name__)
load_dotenv()

class VectorProcessor:
    def __init__(self, embedding_model: Embeddings = None):
        self.embedding_model = embedding_model or OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        test_vector = self.embedding_model.embed_query("test")
        self.dimension = len(test_vector)
        logger.info(f"Embed Model successfully loaded. Its dimensions is: {self.dimension}")

    def add_vectors_to_chunks(self, chunks: List[Dict]) -> List[Dict]:
        logger.info(f"Generating embeddings for {len(chunks)} docs...")
        texts = [doc["content"] for doc in chunks]
        try:
            vectors = self.embedding_model.embed_documents(texts)
            for i, doc in enumerate(chunks):
                doc["vector"] = vectors[i]
            return chunks
        except Exception as e:
            logger.error(f"Error when tried to generate embeddings: {e}")
            raise