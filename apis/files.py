import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, Request
from core.files import Storage
from core.logger import logger
from core.rate_limiter import limiter
from core.responses import responsify
from core.auth import get_current_active_user
from models.users import UserResponse
from models.files import FileResponseModel, FileResponseErrorModel
from repositories.files import FileRepository


routers = APIRouter(prefix="", tags=["files"])
ACCEPTED_CONTENT_TYPES = ["application/pdf", "image/tiff", "image/png", "image/jpeg"]


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

    uploaded_files = []
    repo = FileRepository()

    for file in files:
        try:
            file_name = file.filename
            name, extension = file_name.split(".")

            if file.content_type not in ACCEPTED_CONTENT_TYPES:
                raise HTTPException(400, f"Invalid file: {file.filename}")

            file_bytes = await file.read()
            response = Storage().upload_file(
                file_name,
                f"users_files/{current_user.id}/{uuid.uuid4()}.{extension}",
                file_bytes,
            )
            logger.log(f"File {name} has been aploaded ->> ", response)
            obj_data = {
                "file_name": file_name,
                "file_type": extension,
                "url": response.get("url", ""),
            }
            obj_id = repo.create(obj_data)
            obj_data["_id"] = obj_id
            uploaded_files.append(FileResponseModel(**obj_data))
            logger.log("End_uploading_file ->> ", file_name)
        except Exception as exc:
            logger.log("Error_uploading_file ->> ", exc)
            logger.log_exc(exc)
            uploaded_files.append(
                FileResponseErrorModel(**{"file_name": file_name, "errors": exc.args})
            )

    return responsify(data=uploaded_files, status_code=status.HTTP_201_CREATED)
