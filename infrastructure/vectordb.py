import logging
from typing import List, Union, Any
from langchain_community.vectorstores import Milvus
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from core.environment import get_environ
from core.logger import logger

class MilvusClient:
    def __init__(self) -> None:
        self.MILVUS_CONNECTION = {
            "uri": get_environ("MILVUS_HOST"),
            "port": get_environ("MILVUS_PORT"),
            "user": get_environ("MILVUS_USER"),
            "password": get_environ("MILVUS_PASSWORD"),
        }

    def store_vectors(
        self,
        docs: List[Document],
        collection_name: str,
        embeddings: Embeddings,
        **kwargs,
    ) -> Milvus:
        # save emveddings to vector DB
        logger.log("storing docs ....")
        vector_store = Milvus.from_documents(
            docs,
            embeddings,
            collection_name=collection_name,
            connection_args=self.MILVUS_CONNECTION,
            **kwargs,
        )

        return vector_store

    def get_vectors(
        self, collection_name: str, embeddings: Embeddings, **kwargs
    ) -> Milvus:
        # Get the embeddings from each document.
        vectors = Milvus(
            embeddings,
            collection_name=collection_name,
            connection_args=self.MILVUS_CONNECTION,
            **kwargs,
        )
        return vectors

    def search_similarity(
        self, vector_db: Milvus, query: Union[str, Any]
    ) -> List[Document]:
        docs = vector_db.similarity_search(query)
        return docs

    def get_retriever(
        self, vectors: Milvus, search_kwargs: dict = {"k": 5}
    ) -> VectorStoreRetriever:
        retriever = vectors.as_retriever(search_kwargs=search_kwargs)
        return retriever

    def get_relevant_documents(
        self, retriever: VectorStoreRetriever, query: str, search_kwargs: dict = {"k": 5}
    ) -> List[Document]:
        docs = retriever.get_relevant_documents(
            query, search_kwargs=search_kwargs)
        return docs
