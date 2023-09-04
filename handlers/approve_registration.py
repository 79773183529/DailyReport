from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text, StateFilter
from lexicon import lexicon_ru
from aiogram import F

from entities.user import Post, User
from keyboards.inline_keyboards import non_registration_users_kb
from data_base.with_db import get_non_register_users, register_the_user
from settings.settings import ADMINS

# Инициализируем роутер уровня модуля
router: Router = Router()


class FSMFillForm(StatesGroup):
    choice_user = State()
    fill_last_name = State()
    fill_post = State()


# Этот хэндлер срабатывает на команду /registration
@router.message(Command(commands='approve'), StateFilter(default_state))
async def process_registration_command(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        await message.answer(text=lexicon_ru.Approve.not_admin)
    else:
        users = get_non_register_users()
        await message.answer(text=lexicon_ru.Approve.choice_user, reply_markup=non_registration_users_kb(users))
        await state.set_state(FSMFillForm.choice_user)


# Принимает callback с номером пользователя и регистрирует его
@router.callback_query(StateFilter(FSMFillForm.choice_user))
async def process_gender_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    # Регистрируем пользователя с номером полученным из callback.data
    print("Callback=", callback.data)
    user = register_the_user(int(callback.data))
    # Удаляем сообщение с кнопками
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text=lexicon_ru.Approve.register_done.format(user.name, user.lastname))
    await state.clear()
    await bot.send_message(user.telegram_id, text=lexicon_ru.Approve.user_answer)




