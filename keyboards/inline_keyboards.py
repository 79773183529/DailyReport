from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from enum import Enum


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Клавиатура формирует список пользователей с регистрацией = Falce
def non_registration_users_kb(users):
    data_dict = {str(user.id): f"Добавить {user.name} {user.lastname}" for user in users}
    return create_inline_kb(width=1, **data_dict)


# Создаёт клавиатуру из названия категорий task
def categories_kb(Category):
    data_dict = {category.name: category.value for category in Category}
    return create_inline_kb(width=1, **data_dict)


# Клавиатура формирует список work_name.text
def work_name_kb(work_names):
    data_dict = {str(work_name.id): f"{work_name.text}" for work_name in work_names}
    data_dict["other"] = "Добавить новую работу"
    return create_inline_kb(width=1, **data_dict)


# Создаёт клавиатуру из названия исполнителей
def contractor_kb(Contractor):
    data_dict = {contractor.name: contractor.value for contractor in Contractor}
    return create_inline_kb(width=1, **data_dict)


def tasks_kb(tasks):
    data_dict = {str(task.id): task.work_name.text for task in tasks}
    return create_inline_kb(width=1, **data_dict)
