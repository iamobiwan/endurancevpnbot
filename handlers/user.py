from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.inline.start import new_user_keyboard, user_keyboard, expired_keyboard
from db.queries.user import get_user, create_user
from db.models import User
from misc import status, messages


async def start(message : types.Message):
    """ Приветствие """
    user: User = get_user(message.from_user.id)

    if not user:
        user: User = create_user(message)

    if user.status == 'created':
        await message.answer(
            messages.WELCOME_NEW.format(name=user.name),
            parse_mode='Markdown',
            reply_markup=new_user_keyboard(user)
        )
    elif user.status == 'expired':
        await message.answer(
            messages.WELCOME_EXPIRED.format(
                name=user.name,
                status=status.USER_STATUS.get(user.status),
                expire_date=user.expires_at
                ),
            parse_mode='Markdown',
            reply_markup=expired_keyboard(user)
        )
    else:
        await message.answer(
            messages.WELCOME_USER.format(
                name=user.name,
                status=status.USER_STATUS.get(user.status),
                expire_date=user.expires_at
                ),
            parse_mode='Markdown',
            reply_markup=user_keyboard(user)
        )


def register_user_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
