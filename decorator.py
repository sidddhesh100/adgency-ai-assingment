import json
from functools import wraps
from http import HTTPStatus

import jwt
from flask import Response, current_app, request, session


def jwt_authentication(*args, **kw):
    def wrapper(endpoint_method):
        @wraps(endpoint_method)
        def wrapped(*endpoint_args, **endpoint_kw):
            # This is what I want I want to do. Will not work.
            # g.skip_authorization = getattr(endpoint_method, '_skip_authorization', False)
            if "Authorization" in request.headers and request.headers["Authorization"][0:6] == "Bearer":
                token = request.headers["Authorization"][7:]

                try:
                    # decoding the payload to fetch the stored details
                    data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms="HS256")
                except Exception as e:
                    return Response(
                        json.dumps(
                            {
                                "status": False,
                                "message": "Please provice a valid toke",
                                "allErrorMessage": e.args,
                            }
                        ),
                        status=HTTPStatus.UNAUTHORIZED,
                        content_type="application/json",
                    )
                user = current_app.config["MASTER_DB_CON"]["user"].find_one({"user_id": data.get("user_id")})
                if user:
                    user.pop("created_at")
                    user.pop("_id")
                    session["user"] = user
                    return endpoint_method(*endpoint_args, **endpoint_kw)
                else:
                    return Response(
                        json.dumps(
                            {
                                "status": False,
                                "message": "User not found",
                            }
                        ),
                        status=HTTPStatus.UNAUTHORIZED,
                        content_type="application/json",
                    )
            else:
                return Response(
                    json.dumps({"status": False, "message": "Please provide Authorization"}),
                    status=HTTPStatus.UNAUTHORIZED,
                    content_type="application/json",
                )

        return wrapped

    return wrapper


def admin_required(*args, **kwargs):
    def wrapper(endpoint_method):
        @wraps(endpoint_method)
        def wrapped(*endpoint_args, **endpoint_kw):
            user = session["user"] or {}
            if user.get("is_admin"):
                return endpoint_method(*endpoint_args, **endpoint_kw)
            return Response(
                json.dumps({"status": False, "message": "User is not authorized"}),
                status=HTTPStatus.UNAUTHORIZED,
                content_type="application/json",
            )

        return wrapped

    return wrapper
