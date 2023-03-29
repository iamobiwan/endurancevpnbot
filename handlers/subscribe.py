from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from db.models import User
from db.queries.user import get_user, create_user
from keyboards.inline.main import created_user_keyboard, user_keyboard, expired_user_keyboard
from misc import status, messages


async def mysub(callback: types.CallbackQuery):
    user: User = get_user(callback.from_user.id)

    if user.status == 'created':
        await callback.message.edit_text(
            messages.WELCOME_CREATED.format(name=user.name),
            parse_mode='Markdown',
            reply_markup=created_user_keyboard()
        )
    elif user.status == 'expired':
        await callback.message.edit_text(
            messages.WELCOME_EXPIRED.format(
                name=user.name,
                status=status.USER_STATUS.get(user.status),
                expire_date=user.expires_at
                ),
            parse_mode='Markdown',
            reply_markup=expired_user_keyboard()
        )
    else:
        await callback.message.edit_text(
            messages.WELCOME_USER.format(
                name=user.name,
                status=status.USER_STATUS.get(user.status),
                expire_date=user.expires_at
                ),
            parse_mode='Markdown',
            reply_markup=user_keyboard()
        )