from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text, StateFilter

from datetime import date

from lexicon import lexicon_ru

from entities.work_name import Category, WorkName
from entities.task import Contractor, Task

from keyboards.inline_keyboards import categories_kb, work_name_kb, contractor_kb
from keyboards.keyboards import keyboard_with_unit, user_keyboard

from data_base.with_db import get_register_users, get_work_name_by_category, add_new_task, get_task_by_author
from data_base.with_db import add_new_work_name, get_user_by_telegram_id, filter_work_names, get_work_name_by_id

# Инициализируем роутер уровня модуля
router: Router = Router()


class FSMFillForm(StatesGroup):
    waiting_for_choice_contractor = State()
    waiting_for_choice_category = State()
    waiting_for_choice_work_name = State()
    waiting_for_name = State()
    waiting_for_unit = State()
    waiting_for_work_volume = State()
    waiting_for_work_done = State()
    waiting_for_number_of_people = State()
    waiting_for_choice_do = State()


# Этот хэндлер срабатывает на команду /task
@router.message(Command(commands='task'), StateFilter(default_state))
async def process_registration_command(message: Message, state: FSMContext):
    if message.from_user.id not in [user.telegram_id for user in get_register_users()]:
        await message.answer(text=lexicon_ru.Task.not_register)
    else:
        await message.answer(text=lexicon_ru.Task.choice_contractor, reply_markup=contractor_kb(Contractor))
        await state.set_state(FSMFillForm.waiting_for_choice_contractor)


# Принимает callback с выбранным исполнителем и запрашивает категорию
@router.callback_query(StateFilter(FSMFillForm.waiting_for_choice_contractor))
async def process_gender_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    contractor = [x for x in Contractor if x.name == callback.data][0]
    await state.update_data(contractor=contractor)
    # Удаляем сообщение с кнопками
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text=lexicon_ru.Task.choice_category, reply_markup=categories_kb(Category))
    await state.set_state(FSMFillForm.waiting_for_choice_category)


# Принимает callback с выбранной категорией, Находим в БД все задачи с этой категорией и выводим кнопки с перечнем +
# вариант добавить новое задание
@router.callback_query(StateFilter(FSMFillForm.waiting_for_choice_category))
async def process_gender_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    category = [x for x in Category if x.name == callback.data][0]
    await state.update_data(category=category)
    # Удаляем сообщение с кнопками
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    work_names = get_work_name_by_category(str(category))
    work_names = filter_work_names(work_names)
    await callback.message.answer(text=lexicon_ru.Task.choice_work_name, reply_markup=work_name_kb(work_names))
    await state.set_state(FSMFillForm.waiting_for_choice_work_name)


# Принимает callback с выбранной work_name
#  или вариант добавить новое задание
@router.callback_query(StateFilter(FSMFillForm.waiting_for_choice_work_name))
async def process_gender_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    # Удаляем сообщение с кнопками
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text=callback.data)
    if callback.data == "other":
        await callback.message.answer(text=lexicon_ru.Task.add_work_name)
        await state.set_state(FSMFillForm.waiting_for_name)
    else:
        await state.update_data(work_name_id=callback.data)
        await callback.message.answer(text=lexicon_ru.Task.request_number_of_persons,
                                      reply_markup=await user_keyboard(list(range(11))))
        await state.set_state(FSMFillForm.waiting_for_number_of_people)


# Принимаем имя работы - запрашивает ед измерения
@router.message(StateFilter(FSMFillForm.waiting_for_name))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "text"
    await state.update_data(text=message.text)
    await message.answer(text=lexicon_ru.Task.request_unit, reply_markup=await keyboard_with_unit())
    await state.set_state(FSMFillForm.waiting_for_unit)


# Принимаем единицы измерения - запрашивает объём работ по смете
@router.message(StateFilter(FSMFillForm.waiting_for_unit))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "unit"
    await state.update_data(unit=message.text)
    await message.answer(text=lexicon_ru.Task.request_work_volume, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(FSMFillForm.waiting_for_work_volume)


# Принимаем общий объём - запрашивает выполнение в процентах по сегодняшний день
@router.message(StateFilter(FSMFillForm.waiting_for_work_volume))
async def process_name_sent(message: Message, state: FSMContext):
    try:
        volume = float(message.text)
        await state.update_data(volume=volume)
        await message.answer(text=lexicon_ru.Task.request_work_done,
                             reply_markup=await user_keyboard([lexicon_ru.Task.button_zero_percent]))
        await state.set_state(FSMFillForm.waiting_for_work_done)
    except ValueError:
        await message.answer(text=lexicon_ru.Task.request_work_volume_error)


# Принимаем выполнение - записывает работу в БД - запрашивает кол-во людей занятых на производстве
@router.message(StateFilter(FSMFillForm.waiting_for_work_done))
async def process_name_sent(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        work_name = WorkName(
            text=data["text"],
            category=data["category"],
            volume=data["volume"],
            unit=data["unit"],
        )
        if message.text != lexicon_ru.Task.button_zero_percent:
            work_name.done = float(message.text.strip("%"))
        work_name_model = add_new_work_name(work_name)
        await state.update_data(work_name_id=work_name_model.id)
        await message.answer(text=lexicon_ru.Task.request_number_of_persons,
                             reply_markup=await user_keyboard(list(range(11))))
        await state.set_state(FSMFillForm.waiting_for_number_of_people)
    except ValueError:
        await message.answer(text=lexicon_ru.Task.request_work_done_error)


# Принимает кол-во людей - запрашивает действие
@router.message(StateFilter(FSMFillForm.waiting_for_number_of_people))
async def process_name_sent(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        task = Task(
            work_name_id=data["work_name_id"],
            contractor=data["contractor"],
            author_id=get_user_by_telegram_id(message.from_user.id),
            day=date.today(),
            number_of_persons=int(message.text)
        )
        add_new_task(task)
        await message.answer(text=lexicon_ru.Task.choice_do,
                             reply_markup=await user_keyboard([lexicon_ru.Task.button_1, lexicon_ru.Task.button_2]))
        await state.set_state(FSMFillForm.waiting_for_choice_do)
    except ValueError:
        await message.answer(text=lexicon_ru.Task.request_number_of_persons_error)


# Принимает выбор действия - запрашивает следующий таск или завершает и показывает список оформленных тасков
@router.message(StateFilter(FSMFillForm.waiting_for_choice_do))
async def process_name_sent(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == lexicon_ru.Task.button_1:
        work_names = get_work_name_by_category(data["category"])
        work_names = filter_work_names(work_names)
        await message.answer(text=lexicon_ru.Task.choice_work_name, reply_markup=work_name_kb(work_names))
        await state.set_state(FSMFillForm.waiting_for_choice_work_name)
    else:
        tasks_list = get_task_by_author(message.from_user.id)
        await message.answer(text=lexicon_ru.Task.end_of_task)
        counter = total = 0
        for task in tasks_list:
            counter += 1
            total += task.number_of_persons
            work_name = get_work_name_by_id(task.work_name_id)
            await message.answer(text=f"{counter}. {work_name.text} - {task.number_of_persons} человек")
        await message.answer(text=lexicon_ru.Task.total.format(total))
        await message.answer(text=lexicon_ru.Task.end_of_task_if, reply_markup=types.ReplyKeyboardRemove())
        await state.clear()


