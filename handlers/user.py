from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.inline.start import start_keyboard
from db.queries.user import get_user, create_user
from misc import status, messages

async def start(message : types.Message):
    """ Приветствие """
    user = get_user(message.from_user.id)
    if not user:
        user = create_user(message)
        await message.answer(
            messages.WELCOME_NEW.format(name=user.name),
            parse_mode='Markdown',
            reply_markup=start_keyboard(user)
            )
    else:
        pass


async def echo(message : types.Message):
    await message.answer(f'Это эхо сообщение: {message.text}')


def register_user_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(echo)
