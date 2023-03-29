from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import User
from ..buttons import button_dict

def my_sub_keyboard():
    markup = InlineKeyboardMarkup()
    button_list = [
        button_dict.get('extend_sub'),
        button_dict.get('orders'),
        button_dict.get('get_promocode'),
        button_dict.get('back_main')
        ]
    
    for button in button_list:
        markup.row(button)
    
    return markup
