from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text, StateFilter
from lexicon import lexicon_ru
from keyboards.inline_keyboards import categories_kb, tasks_kb
from data_base.with_db import get_register_users, add_task_completed, get_task_by_author, get_work_name_by_id
from data_base.with_db import filter_tasks

# Инициализируем роутер уровня модуля
router: Router = Router()


class FSMFillForm(StatesGroup):
    waiting_for_volume = State()


# цикл: берёт task из списка и запрашивает completed на него
async def cycle(message: Message, state: FSMContext, tasks_list: list):
    task = tasks_list.pop(0)
    work_name = get_work_name_by_id(task.work_name_id)

    await state.update_data(task_list=tasks_list)
    await state.update_data(task=task)

    await message.answer(text=f"Вы сегодня запланировали: {work_name.text} - {task.number_of_persons} человек")
    await message.answer(text=lexicon_ru.Report.volume_at_today.format(work_name.done))
    await state.set_state(FSMFillForm.waiting_for_volume)


# Этот хэндлер срабатывает на команду /report
@router.message(Command(commands='report'), StateFilter(default_state))
async def process_report_command(message: Message, state: FSMContext):
    if message.from_user.id not in [user.telegram_id for user in get_register_users()]:
        await message.answer(text=lexicon_ru.Task.not_register)
    else:
        tasks_list = get_task_by_author(message.from_user.id)
        tasks_list = filter_tasks(tasks_list)
        if not tasks_list:
            await message.answer(text=lexicon_ru.RedactTask.start_no_tasks)
        else:
            await cycle(message, state, tasks_list)


# Принимает сколько процентов выполнено сегодня + сохраняет в БД. Если список Тасков не пуст:
# продолжает цикл
# else:
# завершает FSM
@router.message(StateFilter(FSMFillForm.waiting_for_volume))
async def process_1(message: Message, state: FSMContext):
    try:
        volume = float(message.text.replace(",", ".").strip("%"))
        data = await state.get_data()
        tasks_list = data["task_list"]
        add_task_completed(data["task"], volume)
        if tasks_list:
            await cycle(message, state, tasks_list)
        else:
            await message.answer(text=lexicon_ru.Report.end)
            await state.clear()
    except ValueError:
        await message.answer(text=lexicon_ru.Report.end_error)

