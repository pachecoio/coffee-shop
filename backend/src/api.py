import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import requires_auth
from src.drinks import blueprint as drink_blueprint
from src.error_handlers import AuthError, ApiError
from src.decorators import marshal_with

app = Flask(__name__)
app.db = setup_db(app)
CORS(app)
app.register_blueprint(drink_blueprint)

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
db_drop_and_create_all()


## Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


"""
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

"""

"""
@TODO implement error handler for 404
    error handler should conform to general task above 
"""


"""
@TODO implement error handler for AuthError
    error handler should conform to general task above 
"""


@app.errorhandler(AuthError)
def auth_error(error):
    return (
        jsonify({"success": False, "message": error.message}),
        error.status_code or 401,
    )


@app.errorhandler(ApiError)
def api_error(error):
    return (
        jsonify({"success": False, "message": error.message}),
        error.status_code or 400,
    )
