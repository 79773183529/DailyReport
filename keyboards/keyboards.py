from aiogram.types import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder
from enum import Enum


async def user_keyboard(lst: list) -> ReplyKeyboardMarkup:
    # Создаем список списков с кнопками
    keyboard: list[KeyboardButton] = [
        KeyboardButton(text=el) for el in lst
    ]

    # Инициализируем билдер
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    # Добавляем кнопки в билдер
    builder.row(*keyboard, width=1)

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard: ReplyKeyboardMarkup = builder.as_markup(resize_keyboard=True)
    return my_keyboard


# Клавиатура с единицами измерения
async def keyboard_with_unit():
    keyboard = await user_keyboard(["м", "м2", "м3", "шт"])
    return keyboard


