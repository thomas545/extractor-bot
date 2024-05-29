from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from core.logger import logger
from application.brain.utils import format_docs
from application.brain.prompts import assistant_template
from application.brain.operations import get_llm, get_embeddings
from application.brain.retrievers import COLLECTION_NAME, get_exists_retrievers


def run_rag_chain(query):
    try:
        llm = get_llm()
        llm_prompt = assistant_template()
        retriever = get_exists_retrievers(COLLECTION_NAME, get_embeddings())
        logger.log("retrievers in Rag -> ", retriever)

        logger.log("Start Running RAG -> ", query)
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | llm_prompt
            | llm
            | StrOutputParser()
        )
        logger.log("Finish Running RAG -> ", query)
        return rag_chain.invoke(query)
    except Exception as exc:
        logger.log("Error While Running RAG ->> ", exc.args)
        logger.log_exc(exc)
        return None
