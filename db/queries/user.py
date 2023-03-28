from aiogram import types
from ..connect import session_maker
from ..models import User
from datetime import datetime
from loader import logger


def create_user(message: types.Message):
    """ Создаем пользователя в БД """
    user = User(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    with session_maker() as session:
        session.add(user)
        session.commit()
        logger.info(f'Создан пользователь {user.id}, зовут {user.name}')
    return user

def get_user(telegram_id):
    """ Вытаскиваем пользователя из БД """
    with session_maker() as session:
        user: User = session.query(User).filter(User.telegram_id == telegram_id).first()
        return user
