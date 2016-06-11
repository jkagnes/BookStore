import FlaskBookstore

from FlaskBookstore.models.book import Book


class Cartline(object):
    """description of class"""

    def __init__(self, book, quantity):
        self.book = book
        self.quantity = quantity


