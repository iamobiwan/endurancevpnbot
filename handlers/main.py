from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main import created_user_keyboard, start_main, main_keyboard, expired_user_keyboard
from db.queries.user import get_user, create_user
from db.models import User
from misc import status, messages


async def start(message : types.Message):
    """ Приветствие """
    user: User = get_user(message.from_user.id)

    if not user:
        user: User = create_user(message)

    await message.answer(
        messages.WELCOME.format(name=user.name),
        parse_mode='Markdown',
        reply_markup=start_main()
    )

async def main(callback: types.CallbackQuery):
    """ Главное меню (обработка c inline кнопки)"""
    user: User = get_user(callback.from_user.id)

    if user.status in ['expired', 'outdated']:
        await callback.message.edit_text(
            messages.MAIN_MENU_EXPIRED,
            parse_mode='Markdown',
            reply_markup=expired_user_keyboard()
        )
    if user.status == 'created':
        await callback.message.edit_text(
            messages.MAIN_MENU_CREATED.format(name=user.name),
            parse_mode='Markdown',
            reply_markup=created_user_keyboard()
        )
    else:
        await callback.message.edit_text(
            messages.MAIN_MENU,
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )

async def main_handler(message: types.Message):
    """ Главное меню (обработка c message handler)"""
    user: User = get_user(message.from_user.id)

    if user.status in ['expired', 'outdated']:
        await message.answer(
            messages.MAIN_MENU_EXPIRED,
            parse_mode='Markdown',
            reply_markup=expired_user_keyboard()
        )
    if user.status == 'created':
        await message.answer(
            messages.MAIN_MENU_CREATED.format(name=user.name),
            parse_mode='Markdown',
            reply_markup=created_user_keyboard()
        )
    else:
        await message.answer(
            messages.MAIN_MENU,
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )


def register_main_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(main_handler, commands=['main'])
    dp.register_callback_query_handler(main, text='main')
