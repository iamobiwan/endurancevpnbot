from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.buttons import button_dict
from db.models import Order
from keyboards.callback import order_callback
from services.orders import get_user_orders


def orders_keyboard(user_id, callback: types.CallbackQuery):
    orders = get_user_orders(user_id)
    markup = InlineKeyboardMarkup()
    if orders:
        for order in orders:
            if order.status == 'success':
                smile = '\U00002705'
            else:
                smile = '\U0000231b'
            button_text = f'{smile} №{order.id} от {order.created_at.strftime("%d.%m.%Y %H:%M")} МСК {order.amount}₽'
            markup.row(
                InlineKeyboardButton(text=button_text, callback_data=order_callback.new(action='get', order_id=order.id))
            )
    markup.row(
        InlineKeyboardButton(
            text='\U000025c0 Назад',
            callback_data='back_main'
        )
    )
    return markup

def order_detail_keyboard(order: Order, callback_data: dict):
    markup = InlineKeyboardMarkup()
    
    if order.status != 'success':
        markup.insert(InlineKeyboardButton(text='\U0001f4b0 Донатить', url=order.donate_url))
    
    markup.row(InlineKeyboardButton(text='\U0001f5d1 Удалить', callback_data=order_callback.new(action='delete', order_id=order.id)))

    if callback_data.get('location') == 'get_sub':
        back_callback = 'back_main'
    elif callback_data.get('location') == 'extend_sub':
        back_callback = 'back_my_sub'

    markup.row(InlineKeyboardButton(text='\U000025c0 Назад', callback_data=back_callback))
    return markup