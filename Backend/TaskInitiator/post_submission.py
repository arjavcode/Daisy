import functools

from TaskInitiator import FormResponse_pb2
from TaskInitiator.TaskSchema import FormResponseWithTask, Task

def post_submission(stub):
  def decorator_post_submission(api_func):
    @functools.wraps(api_func)
    def wrapper_post_submission(*args, **kwargs):
      api_response = api_func(*args, **kwargs)
      
      form_response = FormResponse_pb2.FormResponse()
      form_response.id = kwargs['form_id']
      
      for resp in api_response.responses:
        form_response.responses.add(
          question_id=resp.question_id,
          question_text=resp.question_text,
          question_order=resp.question_order,
          response=resp.response
        )
      
      rpc_response = stub.Process(form_response)
      
      tasks = [Task(task_id=task.task_id, response=task.response) for task in rpc_response.tasks]

      final_response = FormResponseWithTask(
        **api_response.dict(),
        tasks=tasks
      )
      
      return final_response
    
    return wrapper_post_submission
  return decorator_post_submission
