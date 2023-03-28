from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import User

activate_trial_button = InlineKeyboardButton(text='\U0000231B Активировать пробный период', callback_data = 'activate_trial')
get_subscribe_button = InlineKeyboardButton(text='\U00002b50 Оформить подписку', callback_data = 'get_subscribe')
get_discount_button = InlineKeyboardButton(text='\U0001f91d Применить промокод', callback_data = 'get_discount')
get_settings_button = InlineKeyboardButton(text='\U0001f527 Получить настройки', callback_data = 'get_settings')
get_promocode_button = InlineKeyboardButton(text='\U0001f91d Мой промокод', callback_data = 'get_promocode')
orders_button = InlineKeyboardButton(text='\U0001f4cb Мои заказы', callback_data = 'show_orders')
instruction_button = InlineKeyboardButton(text='\U0001f4d2 Инструкция', callback_data = 'get_instruction')


def new_user_keyboard(user: User):
    markup = InlineKeyboardMarkup()
    button_list = [activate_trial_button, get_subscribe_button, get_discount_button]
    
    for button in button_list:
        markup.row(button)

    return markup    

def user_keyboard(user: User):
    markup = InlineKeyboardMarkup()
    button_list = [get_settings_button, get_subscribe_button, get_promocode_button]

    for button in button_list:
        markup.row(button)
    
    markup.add(orders_button, instruction_button)
    return markup

def expired_keyboard(user):
    markup = InlineKeyboardMarkup()
    button_list = [get_subscribe_button, get_promocode_button, orders_button]

    for button in button_list:
        markup.row(button)
    
    return markup




