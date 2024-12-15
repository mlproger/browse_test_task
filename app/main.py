from fastapi import FastAPI
import uvicorn
from producer import publish_task

app = FastAPI()


@app.post("/browse")
async def browse(task: dict):
    publish_task(task)
    return {
        "info": "Задача на просмотр url Принята!",
    }


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )