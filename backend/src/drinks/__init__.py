from flask import Blueprint, jsonify
from src.repositories.drink_repository import DrinkRepository
from src.decorators import marshal_with, parse_with
from src.drinks.schemas import DrinkShortSchema, DrinkSchema, DrinkCreateSchema
from src.helpers import DRINK_SUCCESS_TEMPLATE
from src.auth import requires_auth
import json

blueprint = Blueprint("drinks_blueprint", __name__)

repository = DrinkRepository()


@blueprint.route("/drinks", methods=["GET"])
@marshal_with(DrinkShortSchema(many=True), template=DRINK_SUCCESS_TEMPLATE)
def get_drinks():
    return repository.query.all()


@blueprint.route("/drinks-detail", methods=["GET"])
@requires_auth(permission="get:drinks-detail")
@marshal_with(DrinkSchema(many=True), template=DRINK_SUCCESS_TEMPLATE)
def get_drinks_detail(*args):
    return repository.query.all()


@blueprint.route("/drinks", methods=["POST"])
@requires_auth(permission="post:drinks")
@parse_with(DrinkCreateSchema())
@marshal_with(DrinkSchema())
def create_drink(entity, payload):
    return repository.insert(
        title=entity.get("title"), recipe=json.dumps(entity["recipe"])
    )


@blueprint.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth(permission="patch:drinks")
@parse_with(DrinkCreateSchema())
@marshal_with(DrinkSchema())
def update_drink(entity, payload, id):
    return repository.update(
        id, title=entity.get("title"), recipe=json.dumps(entity["recipe"])
    )


@blueprint.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth(permission="delete:drinks")
def delete_drink(payload, id):
    repository.delete(id)
    return jsonify({"success": True, "id": id})
