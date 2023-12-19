from celery import Celery
from dotenv import load_dotenv
import os
import time

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


@celery.task(name="simple_task")
def simple_task(duration:float, val_a:str='Hello', val_b:str="There") -> str:
    time.sleep(duration)
    res = val_a + " " + val_b
    return f"the task lasted for {duration} secs with result: {res}"
