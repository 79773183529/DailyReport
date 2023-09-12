import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu

from handlers import start_handler, registration, approve_registration, task, redact_task, report, create_plan
from handlers import create_report
from data_base.with_db import get_the_users, get_the_planners
from lexicon.lexicon_ru import Remind

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# Загружаем конфиг в переменную config
config: Config = load_config()

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher()


# Добавляем задачу в планировщик
def schedule_jobs():
    scheduler.add_job(send_message_in_time, "interval", minutes=0, seconds=5)
    scheduler.add_job(send_message_to_planners_in_time, "interval", minutes=10, seconds=5)


async def send_message_in_time():
    print("sheduler_job")
    users = get_the_users()
    for user in users:
        await bot.send_message(chat_id=user.telegram_id, text=Remind.report)


async def send_message_to_planners_in_time():
    print("sheduler_job_planners")
    users = get_the_planners()
    for user in users:
        await bot.send_message(chat_id=user.telegram_id, text=Remind.plan)


# Функция конфигурирования и запуска бота
async def main():
    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(start_handler.router)
    dp.include_router(registration.router)
    dp.include_router(approve_registration.router)
    dp.include_router(task.router)
    dp.include_router(redact_task.router)
    dp.include_router(report.router)
    dp.include_router(create_plan.router)
    dp.include_router(create_report.router)

    # запуск планировщика
    scheduler.start()
    schedule_jobs()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot polling")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
