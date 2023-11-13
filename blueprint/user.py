from flask import Blueprint
from http import HTTPStatus

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
    user = app.config["MASTER_DB_CON"]["user"].find_one({"email":data.get("email")})
    if user and user.get("password")==data.get("password"):
        access_toke = ""
        return Response(
            json.dumps({
                "status": True,
                "message": f"user logged-in",
                "access_token": ""
            }),
            status=HTTPStatus.OK,
            content_type="application/json",
            
        )
    return Response(
            json.dumps({
                "status": False,
                "message": f"Invalid password please try agina",
            }),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
            
        )
        
    

@user.route('/logout')
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

    user_exist = True if len(list(app.config["MASTER_DB_CON"]["user"].find({"email":data.get("email")})))>0 else False
    if not user_exist:
        data["user_id"] = str(uuid4())
        data["created_at"] = datetime.now()
        user = User(**data)
        app.config["MASTER_DB_CON"]["user"].insert_one(user.__dict__)
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
    