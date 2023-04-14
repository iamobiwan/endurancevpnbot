from aiogram.types import InlineKeyboardMarkup
from ..buttons import button_dict

def my_sub_keyboard():
    """ Клавиатура для меню 'Моя подписка' """
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

def back_my_sub_keyboard():
    """ Клавиатура с клавишей назад в 'Моя подписка' """
    markup = InlineKeyboardMarkup()
    markup.row(button_dict.get('back_my_sub'))
    return markup