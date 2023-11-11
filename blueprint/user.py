from flask import Blueprint

user = Blueprint("user", __name__, url_prefix="/user/")

@user.route('/add-book', methods=["POST"])
def add_book():
    pass

@user.route('/add-review', methods=["POST"])
def add_review():
    pass

@user.route('/edit-review', methods=["PUT"])
def edit_review():
    pass

@user.route('/delete-review',  methods=["DELETE"])
def delete_review():
    pass