from datetime import date
from entities.user import SqliteEnum


class Contractor(SqliteEnum):
    Akjol = "Бригада Акжола"
    Ovanas = "Бригада Ованеса"
    Santeh = "Сантехники"
    Vent = "Вентиляционщики"
    Conditioner = "Кондиционерщики"
    Electric = "Электрики"
    Low_currenter = "Слаботочники"
    Metall = "Бригада Металлистов"
    Other = "Другие"


class Task:
    def __init__(self, work_name_id: int,
                 contractor: Contractor,
                 day: date,
                 author_id: int,
                 number_of_persons: int = 0,
                 completed=0):
        self._work_name_id = work_name_id
        self._contractor = contractor
        self._day = day
        self.author_id = author_id
        self._number_of_persons = number_of_persons
        self._completed = completed

    @property
    def work_name_id(self):
        return self._work_name_id

    @work_name_id.setter
    def work_name_id(self, value):
        if isinstance(value, int):
            self._work_name_id = value
        else:
            raise ValueError

    @property
    def contractor(self):
        return self._contractor

    @contractor.setter
    def contractor(self, value):
        if isinstance(value, Contractor):
            self._contractor = value
        else:
            raise ValueError

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        if isinstance(value, date):
            self._day = value
        else:
            raise ValueError

    @property
    def number_of_persons(self):
        return self._number_of_persons

    @number_of_persons.setter
    def number_of_persons(self, value):
        if isinstance(value, int):
            self._number_of_persons = value
        else:
            raise ValueError

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed):
        if isinstance(completed, (int, float)):
            self._completed = completed
        else:
            raise ValueError
