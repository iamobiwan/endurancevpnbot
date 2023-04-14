from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main import start_main
from db.connect import session_maker
from loader import logger, config
from misc import messages
from datetime import datetime, timedelta
from services.user import get_user
import settings

async def update_sub_trial(callback: types.CallbackQuery, state: FSMContext):
    """ Оформление пробной подписки """
    user = get_user(callback.from_user.id)
    with session_maker() as session:
        user.status = 'trial'
        user.updated_at = datetime.now()
        user.expires_at = datetime.now() + timedelta(days=settings.TRIAL_SUB_DAYS)
        session.add(user)
        session.commit()
        await state.update_data(
            status=user.status,
            expires_at=user.expires_at.strftime("%d.%m.%Y")
        )