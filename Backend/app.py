from typing import List
import uvicorn
import grpc
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import os

import crud
import schemas
from database import SessionLocal
from TaskInitiator.post_submission import post_submission
from TaskInitiator.TaskSchema import FormResponseWithTask
from TaskInitiator import FormResponse_pb2_grpc

app = FastAPI()
grpc_resources = {}


def get_db_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()


grpc_resources['rpc_address'] = os.getenv('RPC_ADDRESS', 'localhost:50051')
grpc_resources['channel'] = grpc.insecure_channel(grpc_resources['rpc_address'])
print("Connected to gRPC service")


@app.on_event("shutdown")
def close_grpc_channel():
  grpc_resources['channel'].close()
  print("Disconnected from gRPC service.")


@app.get("/")
def index():
  return {'msg': 'Hello world!'}


@app.get("/forms/{form_id}/", response_model=schemas.Form)
def getForm(form_id: str, db: Session = Depends(get_db_session)):
  try:
    form_id = uuid.UUID(form_id)  # raises value error if wrong uuid
    form = crud.getForm(form_id, db)
    if form is None:
      raise ValueError
  except ValueError:
    raise HTTPException(status_code=404, detail="Form not found")
  
  return schemas.Form(id=str(form.id), title=form.title, desc=form.desc, created_on=form.created_on)


@app.post("/forms/", response_model=schemas.Form)
def createForm(form_data: schemas.CreateForm, db: Session = Depends(get_db_session)):
  form = crud.createForm(form_data, db)
  return schemas.Form(id=str(form.id), title=form.title, desc=form.desc, created_on=form.created_on)


@app.get("/forms/{form_id}/questions/", response_model=List[schemas.Question])
def getQuestions(form_id: str, db: Session = Depends(get_db_session)):
  questions = crud.getQuestions(form_id, db)
  return [schemas.Question(id=str(q.id), question_text=q.question_text, question_order=q.question_order,
                           created_on=q.created_on) for q in questions]


@app.post("/forms/{form_id}/questions/", response_model=schemas.Question)
def createQuestion(form_id: str, question_data: schemas.CreateQuestion, db: Session = Depends(get_db_session)):
  try:
    f_id = uuid.UUID(form_id)  # raises value error if wrong uuid
    form = crud.getForm(f_id, db)
    if form is None:
      raise ValueError
  except ValueError:
    raise HTTPException(status_code=404, detail="Form not found")
  
  if crud.getQuestionOnOrder(form_id, question_data.question_order, db) is None:
    question = crud.createQuestion(form_id, question_data, db)
    return schemas.Question(id=str(question.id), question_text=question.question_text,
                            question_order=question.question_order, created_on=question.created_on)
  
  raise HTTPException(status_code=400, detail="That question order already exists.")


@app.get("/forms/{form_id}/responses/", response_model=List[schemas.ShortFormResponse])
def getAllFormResponses(form_id: str, limit: int = 20, offset: int = 0, db: Session = Depends(get_db_session)):
  try:
    f_id = uuid.UUID(form_id)  # raises value error if wrong uuid
    form = crud.getForm(f_id, db)
    if form is None:
      raise ValueError
  except ValueError:
    raise HTTPException(status_code=404, detail="Form not found")
  form_responses = crud.getAllFormResponses(form_id, limit, offset, db)
  return [schemas.ShortFormResponse(id=str(fres.id), responded_on=fres.responded_on) for fres in form_responses]


@app.get("/forms/{form_id}/responses/{response_id}/", response_model=schemas.FormResponse)
def getFormResponse(form_id: str, response_id: str, db: Session = Depends(get_db_session)):
  try:
    f_id = uuid.UUID(form_id)  # raises value error if wrong uuid
    form = crud.getForm(f_id, db)
    if form is None:
      raise ValueError
  except ValueError:
    raise HTTPException(status_code=404, detail="Form not found")
  
  responses = crud.getFormResponse(form_id, response_id, db)
  responded_on = responses[0][0].responded_on
  return schemas.FormResponse(
    id=str(response_id),
    responded_on=responded_on,
    responses=[schemas.Response(question_id=str(resp[1].question_id), response=resp[1].response) for resp in responses]
  )


@app.post("/forms/{form_id}/responses/", response_model=FormResponseWithTask)
@post_submission(FormResponse_pb2_grpc.PostSubmissionStub(channel=grpc_resources['channel']))
def submitForm(form_id: str, responses: schemas.SubmitForm, db: Session = Depends(get_db_session)):
  try:
    f_id = uuid.UUID(form_id)  # raises value error if wrong uuid
    form = crud.getForm(f_id, db)
    if form is None:
      raise ValueError
  except ValueError:
    raise HTTPException(status_code=404, detail="Form not found")
  
  return crud.submitForm(form_id, responses, db)
