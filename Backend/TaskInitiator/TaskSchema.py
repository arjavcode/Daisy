from pydantic import BaseModel
from typing import List

from schemas import FormResponse

class Task(BaseModel):
  task_id: str
  response: str

class FormResponseWithTask(FormResponse):
  tasks: List[Task]
