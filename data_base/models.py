from peewee import *


if __name__ == '__main__':
    db = SqliteDatabase('data_base.db')
else:
    db = SqliteDatabase('data_base/data_base.db')


class BaseModel(Model):
    class Meta:
        database = db


class UserModel(BaseModel):
    class Meta:
        db_table = 'UserModel'

    is_active = BooleanField()
    name = CharField(max_length=40)
    lastname = CharField(max_length=40)
    post = CharField(max_length=40)
    telegram_id = IntegerField()


class WorkNameModel(BaseModel):
    class Meta:
        db_table = 'WorkNameModel'

    category = CharField(max_length=50)
    text = TextField()
    done = FloatField()
    is_done = BooleanField()
    unit = CharField(max_length=10)
    volume = FloatField()


class TaskModel(BaseModel):
    class Meta:
        db_table = 'TaskModel'

    work_name = ForeignKeyField(model=WorkNameModel)
    contractor = CharField(max_length=50)
    date = DateField()
    author = ForeignKeyField(model=UserModel)
    number_of_persons = IntegerField()
    completed = FloatField()


if __name__ == '__main__':
    db.create_tables([UserModel, WorkNameModel, TaskModel])
