from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, Request
from core.logger import logger
from core.rate_limiter import limiter
from core.responses import responsify
from core.auth import get_current_active_user
from models.users import UserResponse
from models.ocr import OcrRequestModel
from application.tasks import ocr_processor_task
from application.files import get_file_object

routers = APIRouter(prefix="", tags=["ocr"])


@routers.post("/ocr/", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def ocr_api(
    request: Request,
    ocr: OcrRequestModel,
    user: Annotated[UserResponse, Depends(get_current_active_user)],
    background_tasks: BackgroundTasks,
):
    """
    Process OCR results with embedding models,
    then upload the embeddings to a vector db for future searches.
    """

    logger.log("Ocr Request -->> ", ocr)
    if not ocr.file_id and not ocr.url:
        raise HTTPException(400, "File id or url is required")

    file_obj = get_file_object(ocr.file_id, ocr.url) # type: ignore
    background_tasks.add_task(ocr_processor_task, file_obj)

    return responsify(
        data={"file": file_obj, "msg": "Processing OCR File."},
        status_code=status.HTTP_200_OK,
    )
