from marshmallow import Schema, fields, validate
from datetime import datetime
from constant import BOOK_GENRE


class UserRegisterSchema(Schema):
    first_name = fields.Str(required=True,validate=validate.Length(min=3, max=15))
    last_name = fields.Str(required=True,validate=validate.Length(min=3, max=15))
    is_admin = fields.Bool(required=True)
    password = fields.Str(required=True,validate=validate.Length(min=8, max=15))
    email = fields.Email(required=True)
    
    
class LoginSchema(Schema):
    password = fields.Str(required=True,validate=validate.Length(min=8, max=15))
    email = fields.Email(required=True)
    
class CreateBookSchema(Schema):    
    name = fields.Str(required=True,validate=validate.Length(min=3, max=150))
    title = fields.Str(required=True,validate=validate.Length(min=3, max=300))
    author = fields.Str(required=True,validate=validate.Length(min=3, max=30))
    genre = fields.Str(required=True,validate=validate.OneOf(BOOK_GENRE))
    publication_year = fields.Int(required=True, validate=validate.Range(min=0, max=datetime.now().year))
    
class AddReviewSchema(Schema):
    book_id = fields.Str(required=True,validate=validate.Length(min=3, max=30))
    user_id = fields.Str(required=True,validate=validate.Length(min=3, max=30))
    reveiw =fields.Str(required=True,validate=validate.Length(min=3, max=300))
    
class UpdateReviewSchema(Schema):
    review_id = fields.Str(required=True,validate=validate.Length(min=3, max=30))
    review =fields.Str(required=True,validate=validate.Length(min=3, max=300))