import json
from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

import bcrypt
import jwt
from flask import Blueprint, Response, current_app, request
from marshmallow.exceptions import ValidationError

from decorator import admin_required, jwt_authentication
from dto.User import User
from schema import LoginSchema, UserRegisterSchema

user = Blueprint("user", __name__, url_prefix="/user/")


@user.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        data = LoginSchema().load(data)
    except ValidationError as e:
        return Response(
            json.dumps(
                {
                    "status": False,
                    "message": "Invalid login credentials",
                    "allErrorMessage": e.messages,
                }
            ),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
        )
    user = current_app.config["MASTER_DB_CON"]["user"].find_one({"email": data.get("email")})
    if user:
        byte_password = data["password"].encode("utf-8")
        is_right_password = bcrypt.checkpw(byte_password, user["password"])

        if is_right_password:
            user["token"] = jwt.encode(
                {"user_id": user["user_id"]},
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            user.pop("password")
            user.pop("_id")
            user["created_at"] = datetime.strftime(user["created_at"], "%c")
            return Response(
                json.dumps({"status": True, "message": "user logged-in", "user": user}),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        return Response(
            json.dumps(
                {
                    "status": False,
                    "message": "Invalid password please try again",
                }
            ),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
        )
    return Response(
        json.dumps(
            {
                "status": False,
                "message": "Invalid user email please try again",
            }
        ),
        status=HTTPStatus.BAD_REQUEST,
        content_type="application/json",
    )


@user.route("/logout")
@jwt_authentication()
def logout():
    pass


@user.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        data = UserRegisterSchema().load(data=data)
    except ValidationError as e:
        return Response(
            json.dumps(
                {
                    "status": False,
                    "message": "Invalid details kindly check and try again",
                    "allErrorMessage": e.messages,
                }
            ),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
        )

    user_exist = True if len(list(current_app.config["MASTER_DB_CON"]["user"].find({"email": data.get("email")}))) > 0 else False
    if not user_exist:
        byte_password = data["password"].encode("utf-8")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(byte_password, salt)
        data["password"] = hash_password
        data["user_id"] = str(uuid4())
        data["created_at"] = datetime.now()
        user = User(**data)
        current_app.config["MASTER_DB_CON"]["user"].insert_one(user.__dict__)
        return Response(
            json.dumps(
                {
                    "status": True,
                    "message": "user created successfully",
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    return Response(
        json.dumps(
            {
                "status": True,
                "message": f"user alredy exist for this email id {data.get('email','')}",
            }
        ),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@user.route("/get-users", methods=["GET"])
@jwt_authentication()
@admin_required()
def get_all_user():
    users = list(current_app.config["MASTER_DB_CON"]["user"].find({}, {"created_at": 0, "_id": 0, "password": 0}))
    if users:
        return Response(
            json.dumps({"status": False, "message": "Users found", "users": users}),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    return Response(
        json.dumps({"status": False, "message": "Users not found"}),
        status=HTTPStatus.NOT_FOUND,
        content_type="application/json",
    )


@user.route("/delete-users", methods=["DELETE"])
@jwt_authentication()
@admin_required()
def remove_user():
    user_id = request.args.get("user_id")
    if user_id:
        user = current_app.config["MASTER_DB_CON"]["user"].find_one({"user_id": user_id})
        if user:
            current_app.config["MASTER_DB_CON"]["user"].delete_one({"user_id": user_id})
            return Response(
                json.dumps(
                    {
                        "status": True,
                        "message": f"User delete for this id {user_id}",
                    }
                ),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        return Response(
            json.dumps({"status": False, "message": f"User found for this id {user_id}"}),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )
    return Response(
        json.dumps({"status": False, "message": "Please provide a user id"}),
        status=HTTPStatus.BAD_REQUEST,
        content_type="application/json",
    )


@user.route("/change-user-authorization", methods=["DELETE"])
@jwt_authentication()
@admin_required()
def change_user_authorization():
    user_id = request.args.get("user_id")
    change_is_admin = request.args.get("change_is_admin")

    if user_id:
        user = current_app.config["MASTER_DB_CON"]["user"].find_one({"user_id": user_id})
        if user:
            current_app.config["MASTER_DB_CON"]["user"].update_one({"user_id": user_id}, {"is_admin": bool(change_is_admin)})
            return Response(
                json.dumps(
                    {
                        "status": True,
                        "message": f"User delete for this id {user_id}",
                    }
                ),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        return Response(
            json.dumps({"status": False, "message": f"User found for this id {user_id}"}),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )
    return Response(
        json.dumps({"status": False, "message": "Please provide a user id"}),
        status=HTTPStatus.BAD_REQUEST,
        content_type="application/json",
    )
