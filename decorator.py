import json
from functools import wraps
from http import HTTPStatus

import jwt
from flask import Response, current_app, request, session


def token_required(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if "Authorization" in request.headers and request.headers["Authorization"][0:6] == "Bearer":
                token = request.headers["Authorization"][7:]
                if not token:
                    return Response(
                        json.dumps({"status": False, "message": "Please provice a valid toke"}),
                        status=HTTPStatus.UNAUTHORIZED,
                        content_type="application/json",
                    )
            else:
                return Response(
                    json.dumps({"status": False, "message": "Please provide Authorization"}),
                    status=HTTPStatus.UNAUTHORIZED,
                    content_type="application/json",
                )
            # return 401 if token is not passed

            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms="HS256")
                user = current_app.config["MASTER_DB_CON"]["user"].find_one({"user_id": data.get("user_id")})
                if user:
                    session["user"] = user
                    return func(*args, **kwargs)
            except Exception:
                return Response(
                    json.dumps({"status": False, "message": "token is invalid"}),
                    status=HTTPStatus.UNAUTHORIZED,
                    content_type="application/json",
                )

        return decorated

    return wrapper


def role_based_authorization(func):
    @wraps
    def wrapper(*args, **kwargs):
        data = request.get_json
        user = current_app.config["MASTER_DB_CON"]["user"].find_one(data.get("user_id"))
        if user.get("is_admin"):
            return func(*args, **kwargs)
        return Response(
            json.dumps({"status": False, "message": "User is not authorized"}),
            status=HTTPStatus.UNAUTHORIZED,
            content_type="application/json",
        )

    return wrapper
