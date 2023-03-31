from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import start_main, back_main_keyboard
from keyboards.inline.subscribe import my_sub_keyboard
from keyboards.inline.plan import plans_keyboard
from keyboards.callback import plan_callback
from services.subscribe import update_sub_trial
from db.models import User
from misc import status, messages
from loader import logger


async def activate_trial(callback: types.CallbackQuery, state: FSMContext):
    """ Активация пробного периода """
    user_data = await state.get_data()

    if user_data.get('status') != 'created':
        await callback.message.edit_text(
            messages.BLOCK_TRIAL,
            reply_markup=start_main()
    )
    else:
        await update_sub_trial(callback, state)
        user_data = await state.get_data()
        await callback.message.edit_text(
            messages.SUCCESS_TRIAL.format(date=user_data.get('expires_at')),
            reply_markup=back_main_keyboard()
        )
        logger.info(f'Пользователь {user_data.get("id")} активировал пробный период сроком до {user_data.get("expires_at")}')

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

async def get_subscribe(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите длительность подписки:', reply_markup=plans_keyboard(callback))


def register_sub_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(activate_trial, text='activate_trial', state='*')
    dp.register_callback_query_handler(my_sub, text='my_sub', state='*')
    dp.register_callback_query_handler(my_sub, text='back_my_sub', state='*')
    dp.register_callback_query_handler(get_subscribe, regexp=r"(^get_sub$|^extend_sub$)", state='*')