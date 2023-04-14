from aiogram import types
from aiogram.dispatcher import FSMContext
from db.connect import session_maker
from db.models import User
from services.user import get_user
from datetime import datetime
import settings
import random
import string


async def check_promocode(message: types.Message, state: FSMContext, promocode: str):
    """ Проверка промокода и начисление скидки """
    with session_maker() as session:
        inviting_user = session.query(User).filter(User.promocode == promocode).first()
        if inviting_user:
            user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
            user.discount += settings.DISCOUNT_FOR_NEW_USER
            user.inviting_user_id = inviting_user.id
            user.updated_at = datetime.now()
            await state.update_data(
                promocode_used=True,
                invite_discount=True
            )
            session.add(user)
            session.commit()
            return True
        else:
            return False
    
def generate_promocode(callback: types.CallbackQuery):
    """ Генерация промокода"""
    with session_maker() as session:
        promocode = ''.join(random.choice(string.ascii_uppercase) for i in range(settings.LEN_PROMOCODE))
        user_promocodes = [item.promocode for item in session.query(User.promocode)]
        while promocode in user_promocodes:
            user_promocodes = [item.promocode for item in session.query(User.promocode)]
        user = session.query(User).filter(User.telegram_id == callback.from_user.id).first()
        user.promocode = promocode
        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
        return promocode
