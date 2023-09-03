import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base

class Task(Base):
  __tablename__ = "tasks"
  
  id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  form_id = sa.Column(UUID(as_uuid=True))
  name = sa.Column(sa.String, nullable=False)
  module = sa.Column(sa.String, nullable=False)
  func = sa.Column(sa.String, nullable=False)
  asyncStatus = sa.Column(sa.Boolean, nullable=False)
