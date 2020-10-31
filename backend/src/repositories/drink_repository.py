from flask import current_app
from src.repositories import BaseRepository
from src.database.models import Drink


class DrinkRepository(BaseRepository):
    name = "Drink"
    model = Drink
