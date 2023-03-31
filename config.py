import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

@dataclass
class TgBot:
    token: str
    admin_ids: List[int]

@dataclass
class Donate:
    y_wallet: str
    y_token: str

@dataclass
class DbConfig:
    host: str
    port: str
    user: str
    password: str
    name: str

@dataclass
class RedisConfig:
    host: str
    port: str

@dataclass
class Config:
    tg_bot: TgBot
    donate: Donate
    db: DbConfig
    redis: RedisConfig

def load_config(path: str = None):
    load_dotenv(path)
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            admin_ids=list(map(int, os.getenv('ADMINS').split(',')))
        ),
        donate=Donate(
            y_token=os.getenv('Y_TOKEN'),
            y_wallet=os.getenv('Y_WALLET')
        ),
        db=DbConfig(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            name=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
        ),
        redis=RedisConfig(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
        )
    )