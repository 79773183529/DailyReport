from aiogram import Bot
from aiogram.types import BotCommand


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [

        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/task',
                   description='План работ'),
        BotCommand(command='/redact_task',
                   description='Редактировать План работ'),
        BotCommand(command='/approve',
                   description='Добавить пользователя'),
        BotCommand(command='/registration',
                   description='Регистрация'),
        BotCommand(command='/report',
                   description="Отчёт по выполненным работам"),
        BotCommand(command='/create_plan',
                   description='Выгрузить эксель с планом работ'),
        BotCommand(command='/create_report',
                   description='Выгрузить эксель с отчётом по работам'),
        BotCommand(command='/exit',
                   description='Выход'),
    ]
    await bot.set_my_commands(main_menu_commands)
