from dataclasses import dataclass
from datetime import datetime


@dataclass(init=True)
class Comment(object):
    comment_id: str
    comment: str
    user_id: str
    review_id: str
    created_at: datetime


@dataclass(init=True)
class Review(object):
    review: str
    book_id: str
    user_id: str
    comment_id: str


@dataclass(init=True)
class Book(object):
    book_id: str
    name: str
    title: str
    author: str
    genre: str
    publication_year: str
    created_at: datetime
