from fastapi import APIRouter, HTTPException, Request
from repositories.users import UserRepository
from core.logger import logger
from core.auth import create_access_token, verify_password
from models.users import UserLogin, UserRequest, UserResponse
from core.rate_limiter import limiter


routers = APIRouter(prefix="/users/auth", tags=["auth"])


@routers.post("/signup/", response_model=UserResponse)
@limiter.limit("3/minute")
async def signup(request: Request, req: UserRequest):
    user_repo = UserRepository()

    if user_repo.get_obj({"email": req.email}):
        raise HTTPException(400, "User Already exists")

    try:
        user_json = req.model_dump()
        user_id = user_repo.create(user_json)
        user_json["_id"] = user_id
        user_json["access_token"] = create_access_token(user_json)
    except Exception as exc:
        logger.log("Signup Error ->> ", exc.args)
        logger.log_exc(exc)
        raise HTTPException(400, exc.args)

    return UserResponse(**user_json)


@routers.post("/login/", response_model=UserResponse)
@limiter.limit("3/minute")
async def login(request: Request, user: UserLogin):
    user_repo = UserRepository()
    email = user.email
    password = user.password
    db_user = user_repo.get_obj({"email": email})

    if not db_user or not verify_password(password, db_user.get("password")):
        raise HTTPException(403, "Invalid User email / Password")

    if not db_user.get("is_active"):
        raise HTTPException(401, "Account is inactive")

    db_user["access_token"] = create_access_token(db_user)
    return db_user
