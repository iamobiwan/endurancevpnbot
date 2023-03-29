from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import start_main
from keyboards.inline.subscribe import my_sub_keyboard
from services.subscribe import update_sub_trial
from db.models import User
from misc import status, messages
from loader import logger


async def trial(callback: types.CallbackQuery, state: FSMContext):
    """ Активация пробного периода подписки """
    user = await state.get_data()

    if user.get('status') != 'created':
        await callback.message.edit_text(
            messages.BLOCK_TRIAL,
            reply_markup=start_main()
    )
    else:
        await update_sub_trial(callback, state)
        user = await state.get_data()
        await callback.message.edit_text(
            messages.SUCCESS_TRIAL.format(date=user.get('expires_at')),
            reply_markup=start_main()
        )
        logger.info(f'Пользователь {user.get("id")} активировал пробный период сроком до {user.get("expires_at")}')

async def my_sub(callback: types.CallbackQuery, state: FSMContext):
    """ Информация о подписке """
    user = await state.get_data()
    await callback.message.edit_text(
        messages.MY_SUB.format(
            status=status.USER_STATUS.get(user.get('status')),
            date=user.get('expires_at')
            ),
        parse_mode='Markdown',
        reply_markup=my_sub_keyboard()
    )


def register_sub_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(trial, text='trial')
    dp.register_callback_query_handler(my_sub, text='my_sub')