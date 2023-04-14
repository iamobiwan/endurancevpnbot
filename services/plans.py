from aiogram import types
from aiogram.dispatcher import FSMContext
from db.connect import session_maker
from db.models import User, Plan


def get_user_and_plans(telegram_id):
    with session_maker() as session:
        plans = session.query(Plan).all()
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        return user, plans