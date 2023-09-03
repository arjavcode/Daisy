import os
from celery import Celery
from dotenv import load_dotenv
import importlib

from tasks import *

load_dotenv()

# celery -A worker.celery worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo

celery = Celery(
  "PostSubmissionAsyncTaskQueue",
  broker=os.environ.get('CELERY_BROKER_URL'),
  backend=os.environ.get('CELERY_BACKEND_URL')
)

@celery.task(name="async_task_wrapper")
def async_task(module_name, entry_point, *args, **kwargs):
  print("async_task fired")
  module = importlib.import_module(f"tasks.{module_name}.{entry_point}")
  TaskClass = getattr(module, entry_point)
  task_instance = TaskClass(*args, **kwargs)
  result = task_instance.run()
  print(result)
  return result
