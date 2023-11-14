from flask import Blueprint, request, current_app, Response, session
from http import HTTPStatus
import jwt
import bcrypt
from marshmallow.exceptions import ValidationError
from schema import UserRegisterSchema, LoginSchema
from http import HTTPStatus
from uuid import uuid4
from datetime import datetime
from dto.User import User
import json
from decorator import token_required

user = Blueprint("user", __name__, url_prefix="/user/")

@user.route('/login')
def login():
    data = request.get_json()
    try:
        data = LoginSchema().load(data)
    except ValidationError as e:
        return Response(
            json.dumps({
                "status": False,
                "message": "Invalid login credentials",
                "allErrorMessage": e.messages
            }),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
            
        )
    user = current_app.config["MASTER_DB_CON"]["user"].find_one({"email":data.get("email")})
    if user:
        byte_password = data["password"].encode("utf-8")
        is_right_password = bcrypt.checkpw(byte_password, user["password"]) 

        if is_right_password:
            user["token"] = jwt.encode(
                        {"user_id": user["user_id"]},
                        current_app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )
            user.pop("password")
            user.pop("_id")
            user["created_at"] = datetime.strftime(user["created_at"], "%c")
            return Response(
                json.dumps({
                    "status": True,
                    "message": f"user logged-in",
                    "user": user
                }),
                status=HTTPStatus.OK,
                content_type="application/json",
                
            )
        return Response(
            json.dumps({
                "status": False,
                "message": f"Invalid password please try again",
            }),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
            
        )
    return Response(
            json.dumps({
                "status": False,
                "message": f"Invalid user email please try again",
            }),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
            
        )
        
    

@user.route('/logout')
@token_required
def logout():
    pass

@user.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    try:
        data = UserRegisterSchema().load(data=data)
    except ValidationError as e:
        return Response(
            json.dumps({
                "status": False,
                "message": "Invalid details kindly check and try again",
                "allErrorMessage": e.messages
            }),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
            
        )

    user_exist = True if len(list(current_app.config["MASTER_DB_CON"]["user"].find({"email":data.get("email")})))>0 else False
    if not user_exist:
        byte_password = data["password"].encode('utf-8') 
        salt = bcrypt.gensalt() 
        hash_password = bcrypt.hashpw(byte_password, salt) 
        data["password"] = hash_password
        data["user_id"] = str(uuid4())
        data["created_at"] = datetime.now()
        user = User(**data)
        current_app.config["MASTER_DB_CON"]["user"].insert_one(user.__dict__)
        return Response(
                json.dumps({
                    "status": True,
                    "message": "user created successfully",
                }),
                status=HTTPStatus.OK,
                content_type="application/json",
                
            )
    return Response(
        json.dumps({
            "status": True,
            "message": f"user alredy exist for this email id {data.get('email','')}",
        }),
        status=HTTPStatus.OK,
        content_type="application/json",
        
    )
    