from aiogram import types
from keyboards.inline.main import start_main
from db.connect import session_maker
from db.models import User
from loader import logger, config
from misc import messages
from datetime import datetime, timedelta
import settings

async def update_sub_trial(user: User, callback: types.CallbackQuery):
    """ Оформление пробной подписки """
    with session_maker() as session:
        user.status = 'trial'
        user.updated_at = datetime.now()
        user.expires_at = datetime.now() + timedelta(days=settings.TRIAL_SUB_DAYS)
        session.add(user)
        session.commit()
        await callback.message.edit_text(
            messages.SUCCESS_TRIAL.format(date=user.expires_at.strftime("%d.%m.%Y")),
            reply_markup=start_main()
        )
        logger.info(f'Пользователь {user.id} активировал пробный период сроком до \
                    {user.expires_at.strftime("%d.%m.%Y")}')