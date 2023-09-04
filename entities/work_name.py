from enum import Enum
from entities.user import SqliteEnum


class Category(SqliteEnum):
    FINISHING = "ОТДЕЛОЧНЫЕ РАБОТЫ"
    ROOF = "КРОВЕЛЬНЫЕ РАБОТЫ"
    FACADE = "ФАСАДНЫЕ РАБОТЫ"
    ELECTRICS = "ЭЛЕКТРОМОНТАЖНЫЕ РАБОТЫ"
    LOW_CURRENT = "СЛАБОТОЧНЫЕ РАБОТЫ"
    METAL = "МОНТАЖ МЕТАЛЛОКОНСТРУКЦИЙ"
    PLUMBING = "САНТЕХНИЧЕСКИЕ РАБОТЫ"
    VENTILATION = "ВЕНТИЛЯЦИЯ"
    CONDITIONING = "КОНИЦИОНИРОВАНИЕ"
    EXTERIOR_GLAZING = "НАРУЖНИЕ ВИТРАЖИ"
    INTERNAL_GLAZING = "ВНУТРЕННИЕ ВИТРАЖИ"
    LANDSCAPING = "БЛАГОУСТРОЙСТВО"
    OTHER = "ДРУГОЕ"


class WorkName:
    def __init__(self, text: str, category: Category, volume: float | int, unit: str = "м2", done=0.00):
        self.text = text
        self._category = category
        self.unit = unit
        self.volume = volume
        self._done = done
        self._is_done = False

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, Category):
            self._category = value
        else:
            raise ValueError

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, value):
        if isinstance(value, (int, float)) and 0 <= value <= 100:
            self._done = value
        elif isinstance(value, (int, float)) and value >= 100:
            self._done = 100.00
            self._is_done = True
        else:
            raise ValueError

    def add_done(self, value):
        self.done += value
