from flask import Blueprint, jsonify
from src.repositories.drink_repository import DrinkRepository
from src.decorators import marshal_with, parse_with
from src.drinks.schemas import DrinkShortSchema, DrinkSchema, DrinkCreateSchema
from src.helpers import DRINK_SUCCESS_TEMPLATE
from src.auth import requires_auth
import json

blueprint = Blueprint("drinks_blueprint", __name__)

repository = DrinkRepository()

## ROUTES
"""
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@blueprint.route("/drinks", methods=["GET"])
@marshal_with(DrinkShortSchema(many=True), template=DRINK_SUCCESS_TEMPLATE)
def get_drinks():
    return repository.query.all()


"""
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@blueprint.route("/drinks-detail", methods=["GET"])
@requires_auth(permission="get:drinks-detail")
@marshal_with(DrinkSchema(many=True), template=DRINK_SUCCESS_TEMPLATE)
def get_drinks_detail(*args):
    return repository.query.all()


"""
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
"""


@blueprint.route("/drinks", methods=["POST"])
@requires_auth(permission="post:drinks")
@parse_with(DrinkCreateSchema())
@marshal_with(DrinkSchema())
def create_drink(entity, payload):
    return repository.insert(
        title=entity.get("title"), recipe=json.dumps(entity["recipe"])
    )


"""
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
"""


@blueprint.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth(permission="patch:drinks")
@parse_with(DrinkCreateSchema())
@marshal_with(DrinkSchema())
def update_drink(entity, payload, id):
    return repository.update(
        id, title=entity.get("title"), recipe=json.dumps(entity["recipe"])
    )


"""
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@blueprint.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth(permission="delete:drinks")
def delete_drink(payload, id):
    repository.delete(id)
    return jsonify({
        "success": True,
        "id": id
    })
