from fastapi import FastAPI
from web_app.router.telegram import tg

app = FastAPI(title="TGApi")

app.include_router(tg)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, port=8079)