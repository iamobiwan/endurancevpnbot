from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import start_main, back_main_keyboard
from keyboards.inline.subscribe import my_sub_keyboard
from keyboards.inline.orders import orders_keyboard
from keyboards.callback import plan_callback
from services.subscribe import update_sub_trial
from db.models import User
from misc import status, messages
from loader import logger


async def show_orders(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.edit_text(
        messages.ORDERS,
        parse_mode='Markdown',
        reply_markup=orders_keyboard(user_data.get('id'), callback)
        )

def register_orders_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(show_orders, regexp=r"(^main_orders$|^sub_orders$)", state='*')