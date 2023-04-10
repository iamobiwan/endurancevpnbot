from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import start_main, back_main_keyboard
from keyboards.inline.subscribe import my_sub_keyboard, back_my_sub_keyboard
from keyboards.inline.orders import orders_keyboard, order_detail_keyboard
from keyboards.callback import order_callback
from services.subscribe import update_sub_trial
from services.orders import get_user_orders, get_order
from db.models import User, Order
from misc import status, messages
from loader import logger


async def show_orders(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    orders = get_user_orders(user_data.get('id'))

    if orders:
        await callback.message.edit_text(
            messages.ORDERS,
            parse_mode='Markdown',
            reply_markup=orders_keyboard(orders)
            )
    else:
        await callback.message.edit_text(
            messages.NO_ORDERS,
            parse_mode='Markdown',
            reply_markup=back_my_sub_keyboard()
            )
        
async def show_order(callback: types.CallbackQuery, callback_data: dict):
    order: Order = get_order(callback_data.get('order_id'))
    await callback.message.edit_text(
        messages.DETAIL_ORDER.format(
                id=order.id,
                amount=order.amount,
                days=order.days,
                status=status.ORDER_STATUS.get(order.status)
            ),
        parse_mode='Markdown',
        reply_markup=order_detail_keyboard(order, callback)
        )

# async def remove_order(callback: types.CallbackQuery, callback_data: dict):
#     delete_order(callback_data.get('order_id'))
#     await callback.answer('Заказ удален')
#     await show_orders(callback)


def register_orders_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(show_orders, text='orders', state='*')
    dp.register_callback_query_handler(show_order, order_callback.filter(action='get'), state='*')