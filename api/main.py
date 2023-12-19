from fastapi import FastAPI, status
from celery import Celery
from dotenv import load_dotenv
import logging
import uvicorn
import os

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

load_dotenv()
app = FastAPI()

celery_task = Celery(__name__)
celery_task.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery_task.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"response": "This works!!"}


@app.get("/tasks/{duration}", status_code=status.HTTP_200_OK)
async def run_task(duration:float):
    r = celery_task.send_task(
        "simple_task",
        kwargs={"duration": duration, "val_a": "Hello", "val_b": "There"}
    )
    logging.info(r.backend)
    return r.id


@app.get("/status/{task_id}", status_code=status.HTTP_200_OK)
async def task_status(task_id: str):
    status = celery_task.AsyncResult(task_id, app=celery_task)
    return {"status": f"task {task_id} is {status.state}"}


@app.get("/result/{task_id}", status_code=status.HTTP_200_OK)
async def task_result(task_id: str):
    result = celery_task.AsyncResult(task_id).result
    return {"result": f"task result: {result}"}


# app.add_api_route()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=os.environ.get("API_SERVER_HOST"),
        port=int(os.environ.get("API_SERVER_PORT")),
        reload=True,
    )
