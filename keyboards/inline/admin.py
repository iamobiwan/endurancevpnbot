from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from db.models import User
from services.orders import get_user_orders
from ..buttons import button_dict


back_admin_menu_button = InlineKeyboardButton(text='\U000025c0 Назад', callback_data='back_admin_menu')

def admin_start_keyboard():
    markup = InlineKeyboardMarkup()
    check_order_button = InlineKeyboardButton(text='\U0001f4b0 Проверить счет', callback_data='admin_enter_order_id')
    extend_sub_button = InlineKeyboardButton(text='\U00002b50 Управление подписками', callback_data='admin_manage_sub')
    add_discount_button = InlineKeyboardButton(text='\U0001f4b5 Добавить скидку', callback_data='admin_set_discount')
    rebuild_server_config = InlineKeyboardButton(text='\U0001f6e0 Обновить конфигурацию серверов', callback_data='admin_rebuild_server_config')
    test_btn = InlineKeyboardButton(text='\U0001f6e0 Тест кнопка', callback_data='admin_test')
    reset_vpn = InlineKeyboardButton(text='\U0001f310 Обнулить VPN', callback_data='admin_reset_vpn')
    markup.row(check_order_button)
    markup.row(extend_sub_button)
    markup.row(add_discount_button)
    markup.row(rebuild_server_config)
    # markup.row(test_btn)
    markup.row(reset_vpn)
    return markup

def admin_user_sub_keyboard():
    markup = InlineKeyboardMarkup()
    extend_sub_button = InlineKeyboardButton(text='\U0001f44d Продлить подписку', callback_data='admin_extend_sub')
    end_sub_button = InlineKeyboardButton(text='\U0001f44e Отменить подписку', callback_data='admin_end_sub')
    markup.row(extend_sub_button)
    markup.row(end_sub_button)
    return markup

def back_admin_start_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(back_admin_menu_button)
    return markup