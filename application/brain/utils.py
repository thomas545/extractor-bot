from typing import List
from langchain.schema import Document
from core.logger import logger


def format_docs(docs: List[Document]) -> str:
    try:
        return "\n".join(doc.page_content for doc in docs)
    except Exception as exc:
        logger.log("format_docs - failed error ->> ")
        logger.log_exc(exc)
        return ""
