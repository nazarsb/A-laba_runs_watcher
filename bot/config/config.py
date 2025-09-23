from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    albg_users: list[int]
    admins: list[int]

@dataclass
class RedisConfig:
    port: int
    host: str

@dataclass
class Logs:
    format: str
    level: int

@dataclass
class DbConfig:
    is_echo: bool
    pg_user: str
    pg_password: str
    pg_host: str
    pg_port: int
    pg_db_name: str

@dataclass
class Config:
    bot: TgBot
    db: DbConfig
    redis: RedisConfig
    logs: Logs



def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env()

    return Config(
        bot=TgBot(
            token=env('TOKEN'),
            albg_users=list(map(int, env.list('ALBG_IDS'))),
            admins=list(map(int, env.list('ADMINS'))),
        ),
        redis=RedisConfig(
            port=env('REDIS_PORT'),
            host=env('REDIS_HOST')
        ),
        logs = Logs(
            format=env('LOGS_FORMAT'),
            level=env('LOGS_LEVEL')
        ),
        db = DbConfig(
            is_echo=env('IS_ECHO'),
            pg_user=env('POSTGRES_USER'),
            pg_password=env('POSTGRES_PASSWORD'),
            pg_host=env('POSTGRES_HOST'),
            pg_port=env('POSTGRES_PORT'),
            pg_db_name=env('POSTGRES_DB'),

        )
    )