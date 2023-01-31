from flask import send_file
from ast import stmt
import os
from typing import List
from uuid import UUID, uuid4
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

from db.app_db import engine, comment
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.view_models import CommentCreate


comment_status = [
    "Pending Review", "Approved", "Suspended"
]


def get_comments(search_string: str = '', status: int = -1):
    session = Session(engine)
    stmt = select(comment)
    comments_result = session.scalars(stmt).all()

    search_string = search_string.lower()
    
    return_value = []
    count = 0
    for result in comments_result:
        can_add: bool = True
        if status != -1 and result.status is not status:
            can_add = False

        if can_add:
            # Check for search_string
            if search_string == '':
                count+=1
                return_value.append({count: result.serialize()})
            else:
                can_add = False
                if (search_string in result.name.lower() or 
                    search_string in result.id.lower() or
                    search_string in str(result.comment.lower()) or 
                    search_string in str(result.address.lower())):
                    can_add = True

                if can_add:
                    count+=1
                    return_value.append({count: result.serialize()})

    # print(return_value)
    return {'comments': return_value}


def get_comment(id: str):
    session = Session(engine)
    stmt = select(comment).where(comment.id == id)
    result = session.scalars(stmt).first()
    return result


def create_comment(_comment: CommentCreate):
    id = str(uuid4())[:6]
    while get_comment(id) is not None:
        id = str(uuid4())[:6]

    with Session(engine) as session:    
        obj = comment(
            id=id,
            name=_comment.name,
            address=_comment.address,
            comment=_comment.comment,
            status=0
        )
        session.add(obj)
        session.commit()
    return {"id": id, "message": 'success'}


def delete(_id: str):
    _comment = get_comment(_id)
    if _comment is None:
        raise NotFound(f"Comment with id:{_id} not found")


    with Session(engine) as session:   
        obj = session.scalars(select(comment).where(
            comment.id == _id)).first()
        session.delete(obj)
        session.commit()
        session.flush()
    return {"message": "Comment deleted"}


def change_status(_id: str, status: int):
    comment_result = get_comment(_id)
    if comment_result is None:        
        raise NotFound(f"Comment with id:{_id} not found")

    with Session(engine) as session:    
        _comment = session.scalars(select(comment).where(comment.id == _id)).first()
        _comment.status=status
        session.commit()
        
    return {"message": "Comment status updated"}
