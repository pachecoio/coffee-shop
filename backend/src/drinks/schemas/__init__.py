from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import json


class DrinkSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    recipe = fields.Method("_build_recipes")

    def _build_recipes(self, obj):
        return json.loads(obj.recipe)


class DrinkShortSchema(DrinkSchema):
    def _build_recipes(self, obj):
        return [
            [
                {"color": r["color"], "parts": r["parts"]}
                for r in json.loads(obj.recipe)
            ]
        ]


class RecipeSchema(Schema):
    name = fields.String()
    color = fields.String()
    parts = fields.Integer()


class DrinkCreateSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    recipe = fields.List(fields.Nested(RecipeSchema), required=True)
