from dataclasses import dataclass
from typing import List

@dataclass(init=True)
class Review(object):
    review: str
    book_id: str
    user_id: str


@dataclass(init=True)
class Book(object):
    book_id : str
    name : str
    reviews : str
    title: str
    author: str
    # year should be less than or equal to current year
    publication_year: str
    reviews: List[Review]