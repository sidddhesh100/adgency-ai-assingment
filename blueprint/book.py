import json
from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

from flask import Blueprint, Response, current_app, request, session
from marshmallow.exceptions import ValidationError

from decorator import admin_required, jwt_authentication
from dto.Book import Book, Comment, Review
from schema import (
    AddComentSchema,
    AddReviewSchema,
    CreateBookSchema,
    FilterBookSchema,
    UpdateReviewSchema,
)

book = Blueprint("book", __name__, url_prefix="/book/")


@book.route("/search", methods=["GET"])
@jwt_authentication()
def search_book():
    """
    find books by title, author, or genre.

    """
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")
    if not title and not author and not genre:
        return Response(
            json.dumps(
                {
                    "status": False,
                    "message": "Please provide search attributes such as title, author, genre",
                },
            ),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
        )
    query = {"$or": []}
    if title:
        query["$or"].append({"title": {"$regex": f"{title}", "$options": "i"}})
    if author:
        query["$or"].append({"author": {"$regex": f"{author}", "$options": "i"}})
    if genre:
        query["$or"].append({"genre": {"$regex": f"{genre}", "$options": "i"}})
    book = list(current_app.config["MASTER_DB_CON"]["book"].find(query, {"_id": 0, "created_at": 0}))
    if len(book) > 0:
        return Response(
            json.dumps(
                {"status": True, "message": "Result found", "result": book},
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    return Response(
        json.dumps(
            {"status": False, "message": "data not found"},
        ),
        status=HTTPStatus.NOT_FOUND,
        content_type="application/json",
    )


@book.route("/filter", methods=["GET"])
@jwt_authentication()
def filter_book():
    """
    filter books by rating, genre, or publication year.

    """

    data = request.args
    try:
        data = FilterBookSchema().load(data)
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
    query = {}
    if data.get("rating", None):
        query["rating"] = data.get("rating", "")
    if data.get("publication_year", None):
        query["publication_year"] = data.get("publication_year", "")
    if data.get("genre", None):
        query["genre"] = data.get("genre", "")
    book = list(current_app.config["MASTER_DB_CON"]["book"].find(query, {"_id": 0, "created_at": 0}))
    if len(book) > 0:
        return Response(
            json.dumps(
                {"status": True, "message": "Result found", "result": book},
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    return Response(
        json.dumps(
            {"status": False, "message": "data not found"},
        ),
        status=HTTPStatus.NOT_FOUND,
        content_type="application/json",
    )


@book.route("/ratings", methods=["PUT"])
# @jwt_authentication()
def update_rating_of_book():
    """
    ratings by user on book
    """

    pipeline = [
        {
            "$lookup": {
                "from": "review",
                "localField": "book_id",
                "foreignField": "book_id",
                "as": "book_reviews",
            }
        },
        {"$unwind": "$book_reviews"},
        {
            "$group": {
                "_id": "$book_id",
                "average_rating": {"$avg": "$book_reviews.rating"},
            }
        },
    ]
    rating = list(current_app.config["MASTER_DB_CON"]["review"].aggregate(pipeline))
    for i in rating:
        current_app.config["MASTER_DB_CON"]["book"].update_one(
            {"book_id": i.get("book_id")}, {"$set": {"rating": i.get("rating", 0)}}
        )
    return Response(
        json.dumps({"status": True, "message": "ratings updated"}),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@book.route("/create", methods=["POST"])
@jwt_authentication()
def add_book():
    data = request.get_json()
    try:
        data = CreateBookSchema().load(data)
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
    data["created_at"] = datetime.now()
    data["book_id"] = str(uuid4())
    data["user_id"] = session.get("user", {}).get("user_id", "")
    data["rating"] = 0
    book = Book(**data)
    current_app.config["MASTER_DB_CON"]["book"].insert_one(book.__dict__)
    book.created_at = datetime.strftime(book.created_at, "%c")
    del book._id
    return Response(
        json.dumps({"status": True, "message": "Book created", "book": book.__dict__}),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@book.route("/review", methods=["POST"])
@jwt_authentication()
def add_review():
    data = request.get_json()
    try:
        data = AddReviewSchema().load(data)
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
    user = session["user"]
    book_exist = current_app.config["MASTER_DB_CON"]["book"].find_one({"book_id": data.get("book_id", "")})
    if not user:
        return Response(
            json.dumps(
                {
                    "status": True,
                    "message": f"user not exist for this  user_id {data.get('user_id','')}",
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    if not book_exist:
        return Response(
            json.dumps(
                {
                    "status": True,
                    "message": f"user not exist for this  book_id {data.get('book_id','')}",
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )

    data["created_at"] = datetime.now()
    data["review_id"] = str(uuid4())
    review = Review(**data)
    current_app.config["MASTER_DB_CON"]["review"].insert_one(review.__dict__)
    review.created_at = datetime.strftime(review.created_at, "%c")
    del review._id
    return Response(
        json.dumps(
            {
                "status": True,
                "message": f"review added for the this book id {data.get('book_id', '')}",
                "data": review.__dict__,
            }
        ),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@book.route("/review", methods=["PUT"])
@jwt_authentication()
def edit_review():
    data = request.get_json()
    try:
        data = UpdateReviewSchema().load(data)
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

    review = current_app.config["MASTER_DB_CON"]["review"].find_one({"review_id": data.get("review_id")})
    if review:
        user = session["user"]
        if review.get("user_id") == user.get("user_id"):
            current_app.config["MASTER_DB_CON"]["review"].update_one(
                {"review_id": data.get("review_id")},
                {"$set": {"review": data.get("review")}},
            )
            return Response(
                json.dumps(
                    {
                        "status": True,
                        "message": f"review updated for the this book id {review.get('book_id', '')}",
                    }
                ),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        return Response(
            json.dumps(
                {
                    "status": True,
                    "message": "This review is not your you can't delete this",
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    return Response(
        json.dumps(
            {
                "status": False,
                "message": f"Review not found for this review id {data.get('review_id')}",
            }
        ),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@book.route("/review", methods=["DELETE"])
@jwt_authentication()
def delete_review():
    review_id = request.args.get("review_id")
    if not review_id:
        return Response(
            json.dumps({"status": False, "message": "Invalid review id"}),
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
        )
    review = current_app.config["MASTER_DB_CON"]["review"].find_one({"review_id": review_id})
    if review:
        user = session["user"]
        if review.get("user_id") == user.get("user_id"):
            current_app.config["MASTER_DB_CON"]["review"].delete_one({"review_id": review_id})
            return Response(
                json.dumps(
                    {
                        "status": True,
                        "message": f"review deleted for this book id {review.get('book_id', '')}",
                    }
                ),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        return Response(
            json.dumps(
                {
                    "status": True,
                    "message": "This review is not your you can't delete this",
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    return Response(
        json.dumps(
            {
                "status": False,
                "message": f"Review not found for this review id {review_id}",
            }
        ),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@book.route("/add-comment-on-review", methods=["POST"])
@jwt_authentication()
def comment_on_review():
    data = request.get_json()
    try:
        data = AddComentSchema().load(data)
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
    # user_exist = current_app.config["MASTER_DB_CON"]["user"].find_one({"user_id": data.get("user_id", "")})
    review = current_app.config["MASTER_DB_CON"]["review"].find_one({"review_id": data.get("review_id")})
    # if user_exist and review:
    if review:
        data["comment_id"] = str(uuid4())
        data["created_at"] = datetime.now()
        comment = Comment(**data)
        current_app.config["MASTER_DB_CON"]["comment"].insert_one(comment.__dict__)
        comment.created_at = datetime.strftime(comment.created_at, "%c")
        del comment._id
        return Response(
            json.dumps(
                {
                    "status": True,
                    "message": f"comment added for this review id {data.get('review_id', '')}",
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )

    response = Response(
        json.dumps(
            {
                "status": False,
                "message": f"Review not found for his reveiew id {data.get('review_id')}",
            }
        ),
        status=HTTPStatus.BAD_REQUEST,
        content_type="application/json",
    )
    return response


@book.route("/moderate-review", methods=["DELETE"])
@jwt_authentication()
@admin_required()
def moderate_review():
    review_id = request.args.get("review_id")
    if review_id:
        review = current_app.config["MASTER_DB_CON"]["review"].find_one({"review_id": review_id})
        if review:
            current_app.config["MASTER_DB_CON"]["review"].delete_one({"review_id": review_id})
            return Response(
                json.dumps(
                    {
                        "status": True,
                        "message": f"admin deleted this review {review_id}",
                    }
                ),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        return Response(
            json.dumps(
                {
                    "status": False,
                    "message": f"Review not found for this id {review_id}",
                }
            ),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )
    return Response(
        json.dumps({"status": False, "message": "Please provide a review id"}),
        status=HTTPStatus.BAD_REQUEST,
        content_type="application/json",
    )


@book.route("/moderate-comment", methods=["DELETE"])
@jwt_authentication()
@admin_required()
def moderate_comment():
    comment_id = request.args.get("comment_id")
    if comment_id:
        comment = current_app.config["MASTER_DB_CON"]["comment"].find_one({"comment_id": comment_id})
        if comment:
            current_app.config["MASTER_DB_CON"]["comment"].delete_one({"comment_id": comment_id})
            return Response(
                json.dumps(
                    {
                        "status": True,
                        "message": f"admin deleted this review {comment_id}",
                    }
                ),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        return Response(
            json.dumps(
                {
                    "status": False,
                    "message": f"Comment not found for this id {comment_id}",
                }
            ),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )
    return Response(
        json.dumps({"status": False, "message": "Please provide a review id"}),
        status=HTTPStatus.BAD_REQUEST,
        content_type="application/json",
    )
