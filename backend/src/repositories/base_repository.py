from flask import jsonify, current_app
from sqlalchemy import exc
from src.error_handlers import ApiError


class BaseRepository(object):
    name = "BaseRepository"

    @property
    def session(self):
        return current_app.db.session

    @property
    def query(self):
        return self.session.query(self.model)

    def get(self, id):
        entity = self.query.get(id)
        if not entity:
            raise ApiError(
                message="{} not found with id {}".format(self.name, id),
                status_code=404,
            )
        return entity

    def insert(self, **kwargs):
        entity = self.model(**kwargs)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, id, **kwargs):
        entity = self.query.get(id)
        if not entity:
            raise ApiError(
                message="{} not found with id {}".format(self.name, id),
                status_code=404,
            )
        for key in kwargs.keys():
            if hasattr(entity, key):
                setattr(entity, key, kwargs.get(key))
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, id):
        entity = self.get(id)
        self.session.delete(entity)
        self.session.commit()
