import datetime
from datetime import time

from data_base.models import UserModel, WorkNameModel, TaskModel
from settings.settings import ACTIVE_PLANNERS

from entities.user import User
from entities.work_name import WorkName
from entities.task import Task


# Принимает аргумент класса User и записывает его в БД
def add_new_user(user: User):
    instance = UserModel(
        name=user.name,
        lastname=user.lastname,
        post=user.post,
        is_active=user.is_active,
        telegram_id=user.telegram_id
    )
    instance.save()


def get_non_register_users():
    instance_list = []
    for instance in UserModel.select().where(UserModel.is_active == False):
        instance_list.append(instance)
    return instance_list


def get_register_users():
    instance_list = []
    for instance in UserModel.select().where(UserModel.is_active == True):
        instance_list.append(instance)
    return instance_list


def get_user_by_telegram_id(telegram_id):
    instance_list = []
    for instance in UserModel.select().where(UserModel.telegram_id == telegram_id):
        instance_list.append(instance)
    print(instance_list)
    return instance_list[-1]


def register_the_user(user_id):
    # Получить пользователя с заданным id
    user = UserModel.get_or_none(UserModel.id == user_id)
    print("user=", user)
    if user:
        # Изменить значение поля is_active на True
        user.is_active = True

        # Сохранить изменения в БД
        user.save()

        print(f"Пользователь с id активирован.")
    else:
        print(f"Пользователь с id не найден.")
    return user


#  возвращает работы по полученной категории
def get_work_name_by_category(category: str):
    instance_list = []
    for instance in WorkNameModel.select().where(WorkNameModel.category == category):
        instance_list.append(instance)
    print(instance_list)
    return instance_list


#  возвращает работы по id
def get_work_name_by_id(the_id: int):
    return WorkNameModel.get_or_none(WorkNameModel.id == the_id)


# Принимает аргумент класса WorkName и записывает его в БД
def add_new_work_name(work_name: WorkName):
    instance = WorkNameModel(
        text=work_name.text,
        category=work_name.category,
        unit=work_name.unit,
        volume=work_name.volume,
        done=work_name.done,
        is_done=False
    )
    instance.save()
    return instance


# принимает work_name и кол-во процентов добавляет их в done
def add_volume_in_work_name(work_name: WorkNameModel, volume: float):
    done = work_name.done
    if done + volume > 100:
        volume = 100 - done
    done += volume
    work_name.done = done
    work_name.save()
    return volume


def add_task_completed(task: TaskModel, completed: float):
    work_name = get_work_name_by_id(task.work_name_id)
    completed = add_volume_in_work_name(work_name, completed)
    task.completed = completed
    task.save()


def add_new_task(task: Task):
    instance = TaskModel(
        work_name=WorkNameModel.get_or_none(WorkNameModel.id == task.work_name_id),
        author=UserModel.get_or_none(UserModel.id == task.author_id),
        contractor=task.contractor,
        date=task.day,
        number_of_persons=task.number_of_persons,
        completed=task.completed
    )

    instance.save()
    print("end add Task")


#  фильтрует список work_names от тех которые уже имеются в сегодняшних тасках
def filter_work_names(work_names_list):
    day = datetime.date.today()
    return [work_name for work_name in work_names_list if not TaskModel.get_or_none(TaskModel.work_name == work_name,
                                                                                    TaskModel.date == day)]


#  фильтрует список task от тех которые уже имеют completed
def filter_tasks(tasks_list):
    return [task for task in tasks_list if not task.completed]


#  Принимает автора - возвращает все его таски за текущий день
def get_task_by_author(author_telegram_id: int):
    author = get_user_by_telegram_id(author_telegram_id)
    day = datetime.date.today()
    instance_list = []
    for instance in TaskModel.select().where(TaskModel.author == author, TaskModel.date == day):
        instance_list.append(instance)
    return instance_list


#  возвращает все таски за текущий день
def get_all_tasks_for_today():
    day = datetime.date.today()
    instance_list = []
    for instance in TaskModel.select().where(TaskModel.date == day):
        instance_list.append(instance)
    return instance_list


#  возвращает task по id
def get_task_by_id(the_id: int):
    return TaskModel.get_or_none(TaskModel.id == the_id)


# Удаляет task by id
def del_task_by_id(task_id):
    instance: TaskModel = get_task_by_id(task_id)
    work_name: WorkName = instance.work_name
    instance.delete_instance()
    return work_name.text


#  Проверяет всех юзеров которые подали план по task, но не отчитались по ним
def get_the_users():
    day = datetime.datetime.today()
    now = datetime.datetime.now()
    the_time = datetime.datetime.combine(day, time(17, 0))
    the_users = []
    if now >= the_time:
        all_users = UserModel.select()
        for user in all_users:
            instances = []
            for instance in TaskModel.select().where(TaskModel.date == day,
                                                     TaskModel.completed == 0.00,
                                                     TaskModel.author == user):
                instances.append(instance)
            if instances:
                the_users.append(user)
                print(user.name)
    return the_users


#  Проверяет всех планировщиков отправили ли они сообщения
def get_the_planners():
    day = datetime.datetime.today()
    now = datetime.datetime.now()
    start_time = datetime.datetime.combine(day, time(8, 0))
    end_time = datetime.datetime.combine(day, time(9, 0))
    the_users = []
    if start_time <= now <= end_time:
        all_users = [ACTIVE_PLANNERS[key] for key in ACTIVE_PLANNERS]
        for telegram_id in all_users:
            user = get_user_by_telegram_id(telegram_id)
            print("user =", user)
            instances = []
            for instance in TaskModel.select().where(TaskModel.date == day, TaskModel.author == user):
                instances.append(instance)
            print("instances=", instances)
            if not instances:
                the_users.append(user)
    return the_users


if __name__ == '__main__':
    get_the_users()
