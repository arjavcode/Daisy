from typing import List, Tuple

from sqlalchemy.orm import Session
import uuid

import models
import schemas


def getForm(form_id: uuid.UUID, db: Session) -> models.Form:
  form = db.query(models.Form).filter(models.Form.id == form_id).first()
  return form


def getFormQuestions(form_id: str, db: Session) -> List[models.Question]:
  questions = db.query(models.Question).filter(models.Question.form_id == form_id).all()
  return questions


def createForm(form_data: schemas.CreateForm, db: Session) -> models.Form:
  form = models.Form(title=form_data.title, desc=form_data.desc)
  db.add(form)
  db.commit()
  db.refresh(form)
  return form


def getQuestions(form_id: str, db: Session) -> List[models.Question]:
  questions = db.query(models.Question).filter(models.Question.form_id == form_id).all()
  return questions


def getQuestionOnOrder(form_id: str, order: int, db: Session) -> models.Question:
  return db.query(models.Question).filter(
    models.Question.form_id == form_id,
    models.Question.question_order == order).first()


def createQuestion(form_id: str, question: schemas.CreateQuestion, db: Session) -> models.Question:
  question = models.Question(question_text=question.question_text, question_order=question.question_order,
                             form_id=form_id)
  db.add(question)
  db.commit()
  db.refresh(question)
  return question


def getAllFormResponses(form_id: str, limit: int, offset: int, db: Session) -> List[models.FormResponse]:
  responses = db.query(models.FormResponse.id, models.FormResponse.responded_on) \
    .filter(models.FormResponse.form_id == form_id) \
    .limit(limit).offset(offset).all()
  
  return responses


# TODO: Check for response_id
def getFormResponse(form_id: str, response_id: str, db: Session) -> List[Tuple[models.FormResponse, models.Response]]:
  responses = db.query(models.FormResponse, models.Response) \
    .join(models.Response, models.FormResponse.id == models.Response.response_id) \
    .filter(models.FormResponse.form_id == form_id, models.Response.response_id == response_id).all()
  return responses


def submitForm(form_id: str, submission: schemas.SubmitForm, db: Session) -> schemas.FormResponse:
  form_response = models.FormResponse(form_id=form_id)
  db.add(form_response)
  db.flush()
  
  responses = [
    models.Response(response_id=form_response.id, question_id=resp.question_id, response=resp.response)
    for resp in submission.responses
  ]
  
  db.bulk_save_objects(responses)
  db.commit()
  
  response_with_questions = db.query(models.Question, models.Response) \
                              .join(models.Response, models.Response.question_id == models.Question.id)\
                              .filter(models.Response.response_id == form_response.id).all()
  
  return schemas.FormResponse(
    id=str(form_response.id),
    responded_on=form_response.responded_on,
    responses=[
      schemas.Response(
        question_id=str(resp[0].id),
        question_text=resp[0].question_text,
        question_order=resp[0].question_order,
        response=resp[1].response
      ) for resp in
      response_with_questions
    ]
  )
