from aiogram import types
from aiogram.dispatcher import FSMContext
from db.connect import session_maker
from db.models import User
from services.user import get_user
import settings
from datetime import datetime


async def check_promocode(message: types.Message, state: FSMContext, promocode: str):
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
