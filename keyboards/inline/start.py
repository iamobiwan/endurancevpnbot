from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import User


def start_keyboard(user: User):
    activate_trial_button = InlineKeyboardButton(text='\U0000231B Активировать пробный период', callback_data = 'activate_trial')
    get_subscribe_button = InlineKeyboardButton(text='\U00002b50 Оформить подписку', callback_data = 'get_subscribe')
    promocode_button = InlineKeyboardButton(text='\U0001f91d Применить промокод', callback_data = 'get_discount')
    orders_button = InlineKeyboardButton(text='\U0001f4cb Мои заказы', callback_data = 'show_orders')
    
    markup = InlineKeyboardMarkup()
    markup.row(activate_trial_button)
    markup.row(get_subscribe_button)
    if user.status == 'created':
        markup.row(promocode_button)
    else:
        pass
    return markup    

