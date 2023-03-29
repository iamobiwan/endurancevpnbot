from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import created_user_keyboard, start_main, main_keyboard, expired_user_keyboard
from db.queries.user import get_user, create_user
from db.queries.common import update_item
from db.models import User
from misc import status, messages

from datetime import datetime, timedelta
import settings



async def trial(callback: types.CallbackQuery):
    user: User = get_user(callback.from_user.id)

    if user.status != 'created':
        await callback.message.edit_text(
        'Вы не можете активировать пробный период!',
        reply_markup=start_main()
    )
    else:
        user.status = 'trial'
        user.updated_at = datetime.now()
        user.expires_at = datetime.now() + timedelta(days=settings.TRIAL_SUB_DAYS)
        await callback.message.edit_text(
            f'Благодарю за активацию пробного периода!\n\n'\
            f'Пробный период заканчивается {user.expires_at.strftime("%d.%m.%Y")}',
            reply_markup=start_main()
        )
        update_item(user)


def register_sub_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(trial, text='trial')