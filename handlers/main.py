from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main import created_user_keyboard, start_main, main_keyboard, expired_user_keyboard
from services.user import get_user, create_user
from db.models import User
from misc import status, messages
from states import BotStates


async def start(message : types.Message, state: FSMContext):
    """ Приветствие """
    user: User = get_user(message.from_user.id)

    if not user:
        user: User = create_user(message)
        await state.update_data(
            id=user.id,
            telegram_id=user.telegram_id,
            status=user.status,
            name=user.name
        )
    await message.answer(
        messages.WELCOME,
        parse_mode='Markdown',
        reply_markup=start_main()
    )

async def main(callback: types.CallbackQuery, state: FSMContext):
    """ Главное меню (обработка c inline кнопки)"""
    user_data = await state.get_data()

    if user_data.get('status') in ['expired', 'outdated']:
        await callback.message.edit_text(
            messages.MAIN_MENU_EXPIRED,
            parse_mode='Markdown',
            reply_markup=expired_user_keyboard()
        )
    elif user_data.get('status') == 'created':
        await callback.message.edit_text(
            messages.MAIN_MENU_CREATED.format(name=user_data.get('name')),
            parse_mode='Markdown',
            reply_markup=created_user_keyboard(user_data.get('id'), callback.data)
        )
    else:
        await callback.message.edit_text(
            messages.MAIN_MENU,
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )

async def main_handler(message: types.Message, state: FSMContext):
    """ Главное меню (обработка c message handler)"""
    user_data = await state.get_data()
    
    if user_data:
        if user_data.get('status') in ['expired', 'outdated']:
            await message.answer(
                messages.MAIN_MENU_EXPIRED,
                parse_mode='Markdown',
                reply_markup=expired_user_keyboard()
            )
        elif user_data.get('status') == 'created':
            await message.answer(
                messages.MAIN_MENU_CREATED.format(name=user_data.get('name')),
                parse_mode='Markdown',
                reply_markup=created_user_keyboard(user_data.get('id'), message.text)
            )
        else:
            await message.answer(
                messages.MAIN_MENU,
                parse_mode='Markdown',
                reply_markup=main_keyboard()
            )


def register_main_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(main_handler, commands=['main'], state='*')
    dp.register_callback_query_handler(main, regexp=r"(^main$|^back_main$)", state='*')
