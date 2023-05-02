from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from db.models import User
from services.orders import get_user_orders
from ..buttons import button_dict

def admin_start_keyboard():
    markup = InlineKeyboardMarkup()
    check_order_button = InlineKeyboardButton(text='\U0001f4b0 Проверить счет', callback_data='admin_enter_order_id')
    markup.row(check_order_button)
    return markup

def back_admin_start_keyboard():
    markup = InlineKeyboardMarkup()
    back_admin_menu_button = InlineKeyboardButton(text='\U000025c0 Назад', callback_data='back_admin_menu')
    markup.row(back_admin_menu_button)
    return markup