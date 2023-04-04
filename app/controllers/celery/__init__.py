from celery import Celery
from config import config

CFG = config()

app = Celery("hello", broker=CFG.REDIS_URL)


@app.task
def hello():
    return "hello world"
