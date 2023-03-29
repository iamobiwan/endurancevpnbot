from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import created_user_keyboard, start_main, main_keyboard, expired_user_keyboard
from services.user import get_user, create_user
from services.subscribe import update_sub_trial
from db.models import User
from misc import status, messages





async def trial(callback: types.CallbackQuery):
    user: User = get_user(callback.from_user.id)

    if user.status != 'created':
        await callback.message.edit_text(
            messages.BLOCK_TRIAL,
            reply_markup=start_main()
    )
    else:
        await update_sub_trial(user, callback)
        


def register_sub_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(trial, text='trial')