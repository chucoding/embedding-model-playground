from enum import Enum

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.naver import ClovaXEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

from app.setting import settings
from app.logger import logger

class EmbeddingType(str, Enum):
    CLOVA = "clova"
    OPENAI = "openai"

class VectorStore:
    def __init__(self, embedding_type: EmbeddingType = EmbeddingType.CLOVA):
        self._store = None
        self._embedding_type = embedding_type
        
    def _get_embeddings(self) -> Embeddings:
        logger.info(f"Loading embeddings for {self._embedding_type}")
        if self._embedding_type == EmbeddingType.CLOVA:
            return ClovaXEmbeddings(
                model='bge-m3',
                api_key=settings.NCP_CLOVASTUDIO_API_KEY
            )
        elif self._embedding_type == EmbeddingType.OPENAI:
            return OpenAIEmbeddings(
                model='text-embedding-3-large',
                api_key=settings.OPENAI_API_KEY
            )
        
    def add_documents(self, documents: list[str]):
        if self._store is None:
            raise RuntimeError("Store not initialized")
        
        docs = [Document(page_content=doc) for doc in documents]
        self._store.add_documents(documents=docs)
        
    def load(self):
        if self._store is None:
            self._store = InMemoryVectorStore(
                self._get_embeddings()
            )
            
    def search(self, query: str, k: int = 1):
        if self._store is None:
            raise RuntimeError("Store not initialized")
        
        results = self._store.similarity_search_with_score(query=query, k=k)
        filtered_results = [(doc, score) for doc, score in results]
        
        # Sort by score in descending order (higher scores first)
        filtered_results.sort(key=lambda x: x[1], reverse=True)
        
        if not filtered_results:
            logger.warning(f"No appropriate document found for search term '{query}'")
            return []
        
        processed_docs = []
        for doc, score in filtered_results:
            doc.metadata['page_content'] = doc.page_content
            doc.metadata['score'] = score
            doc.page_content = ""
            logger.debug(doc.metadata)
            processed_docs.append(doc)
        
        return processed_docs

    def cleanup(self):
        if self._store is not None:
            self._store = None
            logger.info("Successfully cleaned up vector store")