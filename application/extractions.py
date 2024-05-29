from core.logger import logger
from models.extraction import ExtractionResponseErrorModel, ExtractionObjectMapper
from application.brain.workflow import run_rag_chain
from repositories.extraction import ExtractionRepository


def extractor(extraction, user):
    extraction_obj = None
    extraction_repo = ExtractionRepository()

    try:
        extraction_obj = extraction_repo.get_obj(
            {"query": extraction.query, "user_id": user.id, "response": {"$ne": "null"}}
        )
        logger.log("extraction_obj -->> ", extraction_obj)

        if not extraction_obj:
            extraction.response = run_rag_chain(extraction.query)
            logger.log("llm_response -->> ", extraction.response)

            extraction_to_dict = extraction.model_dump()
            extraction_to_dict["user_id"] = user.id
            extraction_to_dict["_id"] = extraction_repo.create(extraction_to_dict)
            extraction_obj = ExtractionObjectMapper(**extraction_to_dict)
    except Exception as exc:
        logger.log("Error while run RAG -> ", exc.args)
        logger.log_exc(exc)
        extraction_obj = ExtractionResponseErrorModel(errors=exc.args)
    return extraction_obj
