from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr
from pydantic.datetime_parse import datetime
from pymysql import Date


class CommentCreate(BaseModel):
    name: str
    comment: str
    address: str
    article_id: str

