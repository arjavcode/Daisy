import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


class Form(Base):
  __tablename__ = "forms"
  
  id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title = sa.Column(sa.String(60), nullable=False)
  desc = sa.Column(sa.String(length=300), default='')
  created_on = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class Question(Base):
  __tablename__ = "questions"
  __table_args__ = (
    sa.UniqueConstraint('form_id', 'question_order'),
  )
  
  id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  form_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("forms.id", ondelete="CASCADE"))
  question_text = sa.Column(sa.String, nullable=False)
  question_order = sa.Column(sa.Integer, nullable=False)
  created_on = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


# class FormQuestion(Base):
#   __tablename__ = "formQuestions"
#   __table_args__ = (
#     sa.UniqueConstraint('form_id', 'question_order'),
#   )
#
#   form_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("forms.id", ondelete="CASCADE"), primary_key=True)
#   question_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
#   question_order = sa.Column(sa.Integer, nullable=False)


class FormResponse(Base):
  __tablename__ = "formResponses"
  
  id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  form_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("forms.id", ondelete="CASCADE"), primary_key=True)
  responded_on = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class Response(Base):
  __tablename__ = "responses"
  
  id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  response_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("formResponses.id", ondelete="CASCADE"))
  question_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
  response = sa.Column(sa.String, nullable=False)
