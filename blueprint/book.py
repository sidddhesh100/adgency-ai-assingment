from flask import Blueprint, request, current_app, Response
from http import HTTPStatus
from schema import CreateBookSchema, AddReviewSchema
from http import HTTPStatus
from datetime import datetime
from uuid import uuid4
from dto.Book import Book, Review
import json
from marshmallow.exceptions import ValidationError
book = Blueprint("book", __name__, url_prefix="/book/")

@book.route('/search', methods=["GET"])
def search_book():
    """
    find books by title, author, or genre.

    """    
    pass

@book.route('/filter', methods=["GET"])
def filter_book():
    """
     filter books by rating, genre, or publication year.

    """    
    pass

@book.route('/ratings', methods=["GET"])
def ratings_of_book():
    """
    ratings by user on book
    """    
    pass

@book.route('/create', methods=["POST"])
def add_book():
    data = request.get_json()
    try:
        data = CreateBookSchema().load(data)
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
    data["created_at"] = datetime.now()
    data["book_id"] = str(uuid4())
    book = Book(**data)
    current_app.config["MASTER_DB_CON"]["book"].insert_one(book.__dict__)
    book.created_at = datetime.strftime(book.created_at, "%c")
    del book._id
    return Response(json.dumps({
        "status": True, "message": "Book created", "book": book.__dict__
    }), status=HTTPStatus.OK, content_type="application/json")
    
@book.route('/review', methods=["POST"])
def add_review():
    data = request.get_json()
    try:
        data = AddReviewSchema().load(data)
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
    user_exist = current_app.config["MASTER_DB_CON"]["user"].find_one({"user_id": data.get("user_id", "")})
    book_exist = current_app.config["MASTER_DB_CON"]["book"].find_one({"book_id": data.get("book_id", "")})
    if not user_exist:
        return Response(
            json.dumps({
                "status": True,
                "message": f"user not exist for this  user_id {data.get('user_id','')}",
            }),
            status=HTTPStatus.OK,
            content_type="application/json",
            
        )
    if not book_exist:
        return Response(
            json.dumps({
                "status": True,
                "message": f"user not exist for this  book_id {data.get('book_id','')}",
            }),
            status=HTTPStatus.OK,
            content_type="application/json",
            
        )
        
    data["created_at"] = datetime.now()
    data["review_id"] = str(uuid4())
    reveiw = Review(**data)
    current_app.config["MASTER_DB_CON"]["review"].insert_one(reveiw.__dict__)
    book.created_at = datetime.strftime(book.created_at, "%c")
    del book._id
    return Response(json.dumps({
        "status": True, "message": f"review added for the this book id {data.get('book_id', '')}"
    }), status=HTTPStatus.OK, content_type="application/json")
        
@book.route('/review', methods=["PUT"])
def edit_review():
    data = request.get_json()
    try:
        data = UpdateReviewSchema().load(data)
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
    review = current_app.config["MASTER_DB_CON"]["review"].find_one({"review_id": data.get("review_id")})
    if review:
        current_app.config["MASTER_DB_CON"]["review"].update({"review_id": data.get("review_id")}, {"$set":{"review": data.get("review")}})
        return Response(json.dumps({
        "status": True, "message": f"review updated for the this book id {review.get('book_id', '')}"
    }), status=HTTPStatus.OK, content_type="application/json")
    return Response(
            json.dumps({
                "status": False,
                "message": f"Review not found for this review id {data.get('review_id')}",
            }),
            status=HTTPStatus.OK,
            content_type="application/json",
            
        )
    
    
@book.route('/review',  methods=["DELETE"])
def delete_review():
    review_id = request.args.get("review_id")
    if not review_id:
        return Response(json.dumps({"status": False, "message": "Invalid review id"}), status=HTTPStatus.BAD_REQUEST, content_type="application/json")
    review = current_app.config["MASTER_DB_CON"]["review"].find_one({"review_id": data.get("review_id")})
    if review:
        current_app.config["MASTER_DB_CON"]["review"].delete_one({"review_id": data.get("review_id")})
        return Response(json.dumps({
        "status": True, "message": f"review deleted for this book id {review.get('book_id', '')}"
    }), status=HTTPStatus.OK, content_type="application/json")
    return Response(
            json.dumps({
                "status": False,
                "message": f"Review not found for this review id {data.get('review_id')}",
            }),
            status=HTTPStatus.OK,
            content_type="application/json",
            
        )