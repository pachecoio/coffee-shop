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


def create_app(db_name=None):
    app = Flask(__name__)
    app.db = setup_db(app, db_name=db_name)
    CORS(app)

    app.db.create_all()

    """
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    """
    # db_drop_and_create_all()

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "unprocessable"}
            ),
            422,
        )

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

    app.register_blueprint(drink_blueprint)
    return app
