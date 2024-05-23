from fastapi import FastAPI
from apis import auth
# from chats.apis import chats_routers

app = FastAPI()


app.include_router(auth.routers)
# app.include_router(chats_routers)



@app.get("/")
def read_root():
    # logger.info("test logger")
    return "Welcome, Extractor App"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
