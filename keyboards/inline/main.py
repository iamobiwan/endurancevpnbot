from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import User
from ..buttons import button_dict


def start_main():
    markup = InlineKeyboardMarkup()
    markup.row(button_dict.get('main'))
    return markup

def created_user_keyboard():
    markup = InlineKeyboardMarkup()
    button_list = [button_dict.get('trial'), button_dict.get('get_sub'), button_dict.get('get_discount')]
    
    for button in button_list:
        markup.row(button)

    return markup    

def expired_user_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(button_dict.get('my_sub'))
    return markup

def main_keyboard():
    markup = InlineKeyboardMarkup()
    button_list = [button_dict.get('get_settings'), button_dict.get('get_instruction'), button_dict.get('my_sub')]

    for button in button_list:
        markup.row(button)
    
    return markup




