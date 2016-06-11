"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

app.secret_key = "bookstore"

import FlaskBookstore.views

#HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 'Could not find what you were looking for', 404