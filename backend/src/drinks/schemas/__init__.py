from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import json


class DrinkSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    recipe = fields.String()


class DrinkShortSchema(DrinkSchema):
    recipe = fields.Method("_build_recipes")

    def _build_recipes(self, obj):
        return [[{'color': r['color'], 'parts': r['parts']} for r in json.loads(obj.recipe)]]
