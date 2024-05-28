import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, Request
from core.files import Storage
from core.logger import logger
from core.rate_limiter import limiter
from core.responses import responsify
from core.auth import get_current_active_user
from models.users import UserResponse
from application.files import upload_files


routers = APIRouter(prefix="", tags=["files"])


@routers.post("/upload/", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def upload_file_api(
    request: Request,
    files: list[UploadFile],
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    """
    Upload Files to Object Storage

    Parameters
    ----------
    files : File
        list of files.
    """

    logger.log("Start_uploading_files ->> ", len(files), files)

    uploaded_files = await upload_files(files, current_user)
    logger.log("End_uploading_files ->> ", len(uploaded_files), uploaded_files)

    return responsify(data=uploaded_files, status_code=status.HTTP_201_CREATED)
