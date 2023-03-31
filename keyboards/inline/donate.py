from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.buttons import button_dict
from db.models import Order
from keyboards.callback import order_callback


def donate_keyboard(order: Order, callback_data: dict):
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