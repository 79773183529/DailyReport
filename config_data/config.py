from dataclasses import dataclass
from environs import Env



@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    id_creator: str  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    # db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), id_creator=env('ID_Creator')))

    # db=DatabaseConfig(database=env('DATABASE'),
    #                   db_host=env('DB_HOST'),
    #                   db_user=env('DB_USER'),
    #                   db_password=env('DB_PASSWORD')
    #                    )


def print_data(config):
    # Выводим значения полей экземпляра класса Config на печать,
    # чтобы убедиться, что все данные, получаемые из переменных окружения, доступны
    print(f'BOT_TOKEN: {config.tg_bot.token}')
    print()


if __name__ == "__main__":
    config = load_config()
    print_data(config)
