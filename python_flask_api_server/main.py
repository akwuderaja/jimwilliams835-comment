from ensurepip import version
from flask import Flask
from flask_restx import Resource, Api
from typing import Optional, List
from uuid import uuid4, UUID
from flask_cors import CORS, cross_origin
from controllers.comment_controller import Comment_controller as comment
from models.email_sender import Send_Guest_To_Support_Email

app = Flask(__name__) #, static_url_path='/static')
#CORS(app)
#@cross_origin(supports_credentials=True)
CORS(app, resources={r"/api/*": {"origins": "*"}}, support_credentials=True, allow_headers=["*"], methods=["*"],
    origins = [
        "http://localhost:3000",
        "https://localhost:3000",
        "http://hempforhealth.net",
        "https://hempforhealth.net",
        "http://pagenotes.com",
        "https://pagenotes.com",
        "37.130.22.21:0",
    ]
)
api = Api(app, version='1.0', title='Rayzer Business Technology', 
    description='A software Tech Company',
    doc="/docs")

# @app.route("/")
# def root():
#     return {"Home": "Welcome Page"}


@app.route("/api/v1/ping", methods = ['GET'])
@cross_origin(supports_credentials=True)
def ping():
    return {"detail": "connected"}



@app.get("/api/v1/comments")
@cross_origin(supports_credentials=True)
def comments():
    return comment.get()


@app.get("/api/v1/comments/<string:comment_id>")
@cross_origin(supports_credentials=True)
def comments_get_by_id(comment_id: str):
    return comment.get_by_id(comment_id)


@app.post("/api/v1/comments")
@cross_origin(supports_credentials=True)
# @token_auth.login_required
def create_comments():
    return comment.post()


@app.delete("/api/v1/comments/<string:id>")
@cross_origin(supports_credentials=True)
def delete_comment(id: str):
    return comment.delete(id)


@app.post("/api/v1/comments/change_status/<string:_id>")
@cross_origin(supports_credentials=True)
def change_status_comment(_id: str):
    return comment.change_status(_id)



@app.post("/api/v1/Send_Support_Email")
@cross_origin(supports_credentials=True)
def SendSupportEmail():
    return Send_Guest_To_Support_Email()


# @app.post("/api/v1/Send_Admin_Support_Email")
# @cross_origin(supports_credentials=True)
# def SendAdminSupportEmail():
#     return user.Send_Admin_Support_Email()



# @app.route("/<string:name>/")
# def say_hello(name):
#     return f"Hello {name}!"


if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=81) #, debug=True)
