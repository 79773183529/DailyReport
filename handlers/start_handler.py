from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, Text
from aiogram import F
from lexicon import lexicon_ru



# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=lexicon_ru.Start.start)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text="помощь")


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='exit'))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text="Вы вышли из диалога", reply_markup=types.ReplyKeyboardRemove())
    # Завершаем машину состояний
    await state.clear()
