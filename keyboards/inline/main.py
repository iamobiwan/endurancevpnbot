from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from db.models import User
from services.orders import get_user_orders
from ..buttons import button_dict


def start_main():
    """ Клавиатура на команду /start"""
    markup = InlineKeyboardMarkup()
    markup.row(button_dict.get('main'))
    return markup

def back_main_keyboard():
    """ Клавиатура для кнопку назад в главное меню """
    markup = InlineKeyboardMarkup()
    markup.row(button_dict.get('back_main'))
    return markup

def created_user_keyboard(user_id):
    """ Клавиатура нового пользователя """
    orders = get_user_orders(user_id)
    markup = InlineKeyboardMarkup()
    button_list = [button_dict.get('activate_trial'), button_dict.get('get_sub'), button_dict.get('get_discount')]
    
    for button in button_list:
        markup.row(button)

    if orders:
        markup.row(InlineKeyboardMarkup(text='\U0001f4cb Мои заказы', callback_data='orders'))

    return markup    

def expired_user_keyboard():
    """ Клавиатура пользователя с истекшей подпиской """
    markup = InlineKeyboardMarkup()
    markup.row(button_dict.get('my_sub'))
    return markup

def main_keyboard():
    """ Клавиатура главного меню """
    markup = InlineKeyboardMarkup()
    button_list = [
        button_dict.get('get_settings'),
        button_dict.get('instruction'),
        button_dict.get('my_sub')
        ]

    for button in button_list:
        markup.row(button)
    
    return markup




