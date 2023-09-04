from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text, StateFilter
from lexicon import lexicon_ru
from aiogram import F

from entities.user import Post, User
from keyboards.keyboards import user_keyboard
from data_base.with_db import add_new_user
from settings.settings import ADMINS


# Инициализируем роутер уровня модуля
router: Router = Router()


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_last_name = State()
    fill_post = State()
    # upload_photo = State()     # Состояние ожидания загрузки фото


# Этот хэндлер срабатывает на команду /registration
@router.message(Command(commands='registration'), StateFilter(default_state))
async def process_registration_command(message: Message, state: FSMContext):
    await message.answer(text=lexicon_ru.Registration.name_request)
    await state.set_state(FSMFillForm.fill_name)


# Принимаем имя - запрашивает фамилию
@router.message(StateFilter(FSMFillForm.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=lexicon_ru.Registration.last_name_request)
    await state.set_state(FSMFillForm.fill_last_name)


# Принимает фамилию - запрашивает должность
@router.message(StateFilter(FSMFillForm.fill_last_name), F.text.isalpha())
async def process_last_name_sent(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    the_keyboard = await user_keyboard([el.value for el in Post])
    await message.answer(text=lexicon_ru.Registration.post_request, reply_markup=the_keyboard)
    await state.set_state(FSMFillForm.fill_post)


# Принимает должность - сохраняем данные в БД. - информирует админов группы
@router.message(StateFilter(FSMFillForm.fill_post))
async def process_post_sent(message: Message, state: FSMContext, bot: Bot):
    if message.text in [el.value for el in Post]:
        data = await state.get_data()
        user = User(
            post=[x for x in Post if x.value == message.text][0],
            name=data["name"],
            lastname=data["last_name"],
            telegram_id=message.from_user.id,
            is_active=False
        )
        add_new_user(user)
        await message.answer(text=lexicon_ru.Registration.fill, reply_markup=types.ReplyKeyboardRemove())
        for admin_id in ADMINS:
            await bot.send_message(admin_id, text=lexicon_ru.Registration.to_admin.format(user))
        # Завершаем машину состояний
        await state.clear()
    else:
        the_keyboard = await user_keyboard([el.value for el in Post])
        await message.answer(text=lexicon_ru.Registration.post_request_error, reply_markup=the_keyboard)






