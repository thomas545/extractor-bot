from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.logger import logger
from core.files import delete_files
from application.brain.loaders import DocumentProcessor
from application.brain.retrievers import create_retrievers, COLLECTION_NAME
from application.brain.operations import get_embeddings


def ocr_processor_task(file_obj):
    logger.log("Start OCR Task -->> ", file_obj)

    try:
        processor = DocumentProcessor(
            file_obj.file_type,
            RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200),
        )
        docs = processor.run_loader(file_obj.url, jq_schema=".analyzeResult.content")

        if docs:
            for document in docs:
                document.metadata["source"] = file_obj.url

        logger.log("local files -->> ", processor.local_files)
        logger.log("Docs -->> ", len(docs))
        logger.log("Docs -->> ", docs[0])

        if processor.local_files:
            delete_files(processor.local_files)  # Delete the downloaded file after use

        create_retrievers(docs, COLLECTION_NAME, get_embeddings())

        logger.log("Finished Storing docs -->> ", len(docs))
    except Exception as exc:
        logger.log_exc(exc)
        logger.log(f"Error in ocr_processor_task -> {exc.args}")
        return False

    return True
