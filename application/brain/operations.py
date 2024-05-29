from fastapi import HTTPException
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from core.environment import get_environ
from core.logger import logger
from .retrievers import get_exists_retrievers, get_relevant_documents


def get_llm():
    if get_environ("OPENAI_API_KEY"):
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    else:
        raise HTTPException(400, "No API key found for either OpenAI or Google")
    return llm


def get_embeddings(service=None):
    if get_environ("OPENAI_API_KEY"):
        embeddings = OpenAIEmbeddings()
        logger.log("OpenAI embeddings Enabled")
    else:
        raise HTTPException(400, "No API key found for either OpenAI or Google")

    return embeddings


def get_documents(query, collection_name, get_docs=True):
    """Get documents that are relevant to the user's query"""

    embeddings = get_embeddings()
    retrievers = get_exists_retrievers(collection_name, embeddings)
    if not retrievers:
        return [], []

    # Get document ids for all available retrievers
    docs = get_relevant_documents(retrievers, query) if get_docs else []
    return retrievers, docs
