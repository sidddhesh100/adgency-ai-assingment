from flask import Blueprint

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