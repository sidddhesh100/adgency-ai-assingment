from flask import Blueprint

user = Blueprint("user", __name__, prefix="user/")

@user.route('/route_name')
def method_name():
    pass