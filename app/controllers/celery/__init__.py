from celery import Celery
from config import config
from app.logger import log

CFG = config()

app = Celery("hello", broker=CFG.REDIS_URL)
app.conf.broker_url = CFG.REDIS_URL
app.conf.result_backend = CFG.REDIS_URL


@app.on_after_configure.connect
def setup_celery(sender: Celery, **kwargs):
    log(log.INFO, "Setup celery from [%s]", CFG.REDIS_URL)
    sender.add_periodic_task(
        10,
        periodic_task.s(),
        name="services check",
    )


@app.task
def periodic_task():
    log(log.WARNING, "Periodic task")
    hello()


@app.task
def hello():
    log(log.WARNING, "WARNING")
    return "hello world"
