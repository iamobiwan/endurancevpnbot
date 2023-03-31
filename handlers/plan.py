from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import start_main, back_main_keyboard
from keyboards.inline.subscribe import my_sub_keyboard
from keyboards.inline.plan import plans_keyboard
from keyboards.inline.orders import order_detail_keyboard
from keyboards.callback import plan_callback
from services.subscribe import update_sub_trial
from services.orders import create_order
from misc import status, messages
from loader import logger

async def select_plan(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    order = await create_order(callback, callback_data, state)

    if order:
        await callback.message.edit_text(
            messages.DETAIL_ORDER.format(
                id=order.id,
                amount=order.amount,
                days=order.days,
                status=status.ORDER_STATUS.get(order.status)
            ),
            parse_mode='Markdown',
            reply_markup=order_detail_keyboard(order, callback_data)
        )
    else:
        await callback.message.edit_text(
            messages.MAX_ORDERS
        )

def register_plan_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(select_plan, plan_callback.filter(), state='*')