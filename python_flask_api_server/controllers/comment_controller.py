from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import models.comment as comment
from models.view_models import CommentCreate


commentCreate = reqparse.RequestParser()
commentCreate.add_argument("name", type=str, help="Comment's name")
commentCreate.add_argument("address", type=str, help="Comment's address")
commentCreate.add_argument("comment", type=str, help="Comment's comment")
commentCreate.add_argument("article_id", type=str, help="Comment's article_id")


commentModel = reqparse.RequestParser()
commentModel.add_argument("comment", type=str, help="comment")
commentModel.add_argument("value", type=str, help="Value")


def getCommentModel():
    _result = request.get_json()
    _comment = CommentCreate(
        name=_result['name'],
        address=_result['address'],
        comment=_result['comment'],
        article_id=_result['article_id'],
    )
    return _comment

class Comment_controller():
    def get():
        search_string: str = request.args.get('search_string', '', str)
        status: int = request.args.get('status', -1, int)
        return comment.get_comments(search_string, status)


    def get_by_id(comment_id: str):
        return comment.get_comment(comment_id).serialize()


    def post():
        # _comment: CommentCreate = commentCreate.parse_args()
        _comment: CommentCreate = getCommentModel()
        return comment.create_comment(_comment)


    # @token_auth.login_required
    def delete(id: str):
        # user_data = get_current_user()
        return comment.delete(id) #, user_data['userID'])

    # @app.post("/api/v1/comments/change_status/{_id}")
    # @token_auth.login_required
    def change_status(_id: str):
        status_model: commentModel = commentModel.parse_args()
        return comment.change_status(_id, int(status_model.value))
