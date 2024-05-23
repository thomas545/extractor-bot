from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.rate_limiter import limiter
from apis import auth

# from chats.apis import chats_routers

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(auth.routers)
# app.include_router(chats_routers)


@app.get("/")
@limiter.limit("5/minute")
async def read_root(request: Request):
    return "Welcome, Extractor App"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
