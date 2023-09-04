from excel.create_report import create_report
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text, StateFilter
from lexicon import lexicon_ru
from keyboards.inline_keyboards import categories_kb, tasks_kb
from data_base.with_db import get_all_tasks_for_today
from data_base.with_db import filter_tasks
from settings.settings import ADMINS

# Инициализируем роутер уровня модуля
router: Router = Router()


class FSMFillForm(StatesGroup):
    waiting_for_volume = State()


# Этот хэндлер срабатывает на команду /report_to_excel
@router.message(Command(commands='report_to_excel'), StateFilter(default_state))
async def process_report_command(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id not in ADMINS:
        await message.answer(text=lexicon_ru.Approve.not_admin)
    else:
        tasks_list = get_all_tasks_for_today()
        filename = create_report(filename="data/templates/report/report.xlsx",
                                 task_list=tasks_list
                                 )
        await message.answer(text=lexicon_ru.CreatePlan.good)
        doc = types.FSInputFile(filename)
        await bot.send_document(message.from_user.id, doc)
