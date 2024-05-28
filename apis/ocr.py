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
async def upload_file_api(
    request: Request,
    ocr: OcrRequestModel,
    user: Annotated[UserResponse, Depends(get_current_active_user)],
    background_tasks: BackgroundTasks,
):
    """
    Upload Files to Object Storage

    Parameters
    ----------
    files : File
        list of files.
    """

    logger.log("Ocr Request -->> ", ocr)
    if not ocr.file_id and not ocr.url:
        raise HTTPException(400, "File id or url is required")

    file_obj = get_file_object(str(ocr.file_id))
    background_tasks.add_task(ocr_processor_task, file_obj)

    return responsify(
        data={"file": file_obj, "msg": "Processing OCR File."},
        status_code=status.HTTP_200_OK,
    )
