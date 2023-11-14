from datetime import datetime

from marshmallow import Schema, fields, validate, validates_schema
from marshmallow.exceptions import ValidationError

from constant import BOOK_GENRE


class UserRegisterSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=3, max=15))
    last_name = fields.Str(required=True, validate=validate.Length(min=3, max=15))
    is_admin = fields.Bool(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=15))
    email = fields.Email(required=True)


class LoginSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=8, max=15))
    email = fields.Email(required=True)


class CreateBookSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    title = fields.Str(required=True, validate=validate.Length(min=3, max=300))
    author = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    genre = fields.Str(required=True, validate=validate.OneOf(BOOK_GENRE))
    publication_year = fields.Int(required=True, validate=validate.Range(min=0, max=datetime.now().year))


class AddReviewSchema(Schema):
    book_id = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    user_id = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    reveiw = fields.Str(required=True, validate=validate.Length(min=3, max=300))
    rating = fields.Decimal(required=True, validate=validate.Range(min=0, max=5))


class UpdateReviewSchema(Schema):
    review_id = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    review = fields.Str(required=True, validate=validate.Length(min=3, max=300))
    rating = fields.Decimal(required=True, validate=validate.Range(min=0, max=5))


class AddComentSchema(Schema):
    user_id = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    review_id = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    comment = fields.Str(required=True, validate=validate.Length(min=3, max=300))


class FilterBookSchema(Schema):
    rating = fields.Decimal(required=False, validate=validate.Range(min=0, max=5))
    genre = fields.Str(required=False, validate=validate.OneOf(BOOK_GENRE))
    publication_year = fields.Int(required=False, validate=validate.Range(min=0, max=datetime.now().year))

    @validates_schema
    def validate(self, data, **kwargs):
        if not data.get("rating") and not data.get("genre") and not data.get("publication_year"):
            raise ValidationError("Please apply any one filter from this rating, genre, publication_year")
