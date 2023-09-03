import datetime
from pydantic import BaseModel
from typing import List, Optional

class CreateQuestion(BaseModel):
  question_order: int
  question_text: str

class Question(CreateQuestion):
  id: str
  created_on: datetime.date
  
  class Config:
    orm_mode = True

class CreateForm(BaseModel):
  title: str
  desc: Optional[str]

  class Config:
    orm_mode = True

class Form(CreateForm):
  id: str
  title: str
  desc: Optional[str]
  created_on: datetime.date
  
  class Config:
    orm_mode = True

class ResponseSubmission(BaseModel):
  question_id: str
  response: str

  class Config:
    orm_mode = True

class Response(BaseModel):
  question_id: str
  question_text: Optional[str]
  question_order: Optional[int]
  response: str
  
  class Config:
    orm_mode = True

class FormResponse(BaseModel):
  id: str
  responses: List[Response]
  responded_on: datetime.date
  
  class Config:
    orm_mode = True

class ShortFormResponse(BaseModel):
  id: str
  responded_on: datetime.date

class SubmitForm(BaseModel):
  responses: List[ResponseSubmission]
  
  class Config:
    orm_mode = True
