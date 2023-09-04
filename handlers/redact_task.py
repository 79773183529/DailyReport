from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text, StateFilter
from lexicon import lexicon_ru
from keyboards.inline_keyboards import categories_kb, tasks_kb
from data_base.with_db import get_register_users, del_task_by_id, get_task_by_author

# Инициализируем роутер уровня модуля
router: Router = Router()


class FSMFillForm(StatesGroup):
    waiting_for_task_id = State()


# Этот хэндлер срабатывает на команду /redact_task
@router.message(Command(commands='redact_task'), StateFilter(default_state))
async def process_registration_command(message: Message, state: FSMContext):
    if message.from_user.id not in [user.telegram_id for user in get_register_users()]:
        await message.answer(text=lexicon_ru.Task.not_register)
    else:
        tasks_list = get_task_by_author(message.from_user.id)
        if not tasks_list:
            await message.answer(text=lexicon_ru.RedactTask.start_no_tasks)
        else:
            await message.answer(text=lexicon_ru.RedactTask.start, reply_markup=tasks_kb(tasks_list))
            await state.set_state(FSMFillForm.waiting_for_task_id)


# Принимает callback с выбранным исполнителем и запрашивает категорию
@router.callback_query(StateFilter(FSMFillForm.waiting_for_task_id))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    task_text = del_task_by_id(int(callback.data))
    # Удаляем сообщение с кнопками
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text=lexicon_ru.RedactTask.del_position.format(task_text))
    await state.clear()



