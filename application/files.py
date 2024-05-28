import uuid
from bson import ObjectId
from fastapi import HTTPException
from core.logger import logger
from core.files import Storage
from models.ocr import OcrObjectMapper
from models.files import FileResponseModel, FileResponseErrorModel
from repositories.files import FileRepository

ACCEPTED_CONTENT_TYPES = ["application/pdf", "image/tiff", "image/png", "image/jpeg"]


def get_file_object(obj_id: str) -> OcrObjectMapper:
    file_repo = FileRepository()
    # file_obj = file_repo.get_obj({"_id": "6654c225e8769fc30206f225"})
    file_obj = OcrObjectMapper(**file_repo.get_obj({"_id": ObjectId(obj_id)}))
    logger.log("File Object -->> ", file_obj)
    return file_obj


async def upload_files(files, current_user) -> list:
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

    return uploaded_files
