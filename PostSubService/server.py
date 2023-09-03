import contextlib

import grpc
from concurrent import futures

import FormResponse_pb2
import FormResponse_pb2_grpc
from database import SessionLocal
import models
from worker import async_task

@contextlib.contextmanager
def get_db_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()


class PostSubmissionServicer(FormResponse_pb2_grpc.PostSubmissionServicer):
  def __init__(self, db):
    self.db = db

  def Process(self, request, context):
    print("Process called")
    form_response = request
    responses = [
      {
        'question_id': response.question_id,
        'question_text': response.question_text,
        'question_order': response.question_order,
        'response': response.response
      }
      for response in form_response.responses
    ]
    
    tasks_list = self.db.query(models.Task).filter(models.Task.form_id == form_response.id).all()
    synced_tasks_list = filter(lambda t: not t.asyncStatus, tasks_list)
    asynced_tasks_list = filter(lambda t: t.asyncStatus, tasks_list)
  
    output = FormResponse_pb2.TaskStatus()
  
    # running all synced tasks
    for task in synced_tasks_list:
      module = __import__(task.module)
      func = getattr(module, task.func)
      result = func(responses)
      output.tasks.add(task_id=task.id, response=str(result))
  
    # firing all async tasks in celery instance
    for task in asynced_tasks_list:
      print("..")
      result = async_task.delay(task.module, task.func, form_id=form_response.id, response=responses)
      output.tasks.add(task_id=str(task.id), response=str(result))
  
    return output
  

def serve():
  with get_db_session() as db:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FormResponse_pb2_grpc.add_PostSubmissionServicer_to_server(
      PostSubmissionServicer(db), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Listening at localhost:50051")
    server.wait_for_termination()


if __name__ == '__main__':
  serve()
