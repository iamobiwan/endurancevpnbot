from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main import start_main
from db.connect import session_maker
from loader import logger, config, dp
from misc import messages
from datetime import datetime, timedelta
from services.user import get_user
from db.models import User
import settings


async def extend_user_sub(edit_user_id, sub_days):
    with session_maker() as session:
        user: User = session.query(User).filter(User.id == edit_user_id).first()
        user_state: FSMContext = dp.current_state(user=user.telegram_id, chat=user.chat_id)
        if user.status in ['subscribed', 'trial']:
            user.expires_at = user.expires_at + timedelta(days=sub_days)
        elif user.status in ['expired', 'outdated']:
            user.expires_at = datetime.now() + timedelta(days=sub_days)
        user.status = 'subscribed'
        await user_state.update_data(
            status=user.status,
            expires_at=user.expires_at.strftime("%d.%m.%Y")
        )
        session.add(user)
        session.commit()
            

async def end_user_sub(edit_user_id):
    pass