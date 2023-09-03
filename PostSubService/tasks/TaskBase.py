import abc
from typing import Dict

class TaskBase(abc.ABC):
  def __init__(self, form_id: str, response: Dict):
    self.form_id = form_id
    self.response = response
  
  @abc.abstractmethod
  def run(self):
    pass
