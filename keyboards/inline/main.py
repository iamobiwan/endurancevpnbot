from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import User
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

def created_user_keyboard():
    """ Клавиатура нового пользователя """
    markup = InlineKeyboardMarkup()
    button_list = [button_dict.get('trial_question'), button_dict.get('get_sub_question'), button_dict.get('get_discount')]
    
    for button in button_list:
        markup.row(button)

    return markup    

def expired_user_keyboard():
    """ Клавиатура пользователя с истекшей подпиской """
    markup = InlineKeyboardMarkup()
    markup.row(button_dict.get('my_sub'))
    return markup

def main_keyboard():
    """ Клавиатура главного меню """
    markup = InlineKeyboardMarkup()
    button_list = [button_dict.get('get_settings'), button_dict.get('get_instruction'), button_dict.get('my_sub')]

    for button in button_list:
        markup.row(button)
    
    return markup




