from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, Request
from core.logger import logger
from core.rate_limiter import limiter
from core.responses import responsify
from core.auth import get_current_active_user
from models.extraction import ExtractionRequestModel
from application.extractions import extractor
from models.users import UserResponse


routers = APIRouter(prefix="", tags=["ocr"])


@routers.post("/extract/", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def extract_api(
    request: Request,
    extraction: ExtractionRequestModel,
    user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    logger.log("Extract Request -->> ", extraction)
    extraction_obj = extractor(extraction, user)
    logger.log("Extract Response -->> ", extraction_obj)

    return responsify(
        data={"response": extraction_obj},
        status_code=status.HTTP_200_OK,
    )
