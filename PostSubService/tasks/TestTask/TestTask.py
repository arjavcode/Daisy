import time

from ..TaskBase import TaskBase

class TestTask(TaskBase):
  def __init__(self, form_id, response):
    super().__init__(form_id, response)

  def run(self):
    print("Task fired...")
    time.sleep(10)
    print(f"Task done!\nResponse = {self.response}")
    return "[TestTask] done"
