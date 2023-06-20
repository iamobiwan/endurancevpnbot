from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import or_, func
from db.connect import session_maker
from db.models import User, Vpn, Server
from keyboards.inline.main import back_main_keyboard
from services.keys import generate_key, public_key
from datetime import datetime
from loader import logger, bot
from subnet import IPv4Network
from misc import messages
import settings


def create_vpn(user: User):
    """ Создаем VPN в БД """
    vpn = Vpn(
        user_id=user.id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    with session_maker() as session:
        session.add(vpn)
        session.commit()

async def change_vpn_status_to_requested(state: FSMContext, user_id):
    with session_maker() as session:
        vpn: Vpn = session.query(Vpn).where(Vpn.user_id == user_id).first()
        vpn.status = 'pending'
        await state.update_data(
            vpn_status='pending'
        )
        session.add(vpn)
        session.commit()

async def send_vpn_settings(user_data):
    with open(f'users/config/endurancevpn_{user_data.get("id")}.conf', 'rb') as config:
        await bot.send_document(
            user_data.get('chat_id'),
            config,
            caption=messages.GET_SETTINGS_SUCCESS,
        )
    # await bot.send_message(
    #     chat_id=user_data.get('chat_id'),
    #     text=
    #     parse_mode='Markdown',
    #     reply_markup=back_main_keyboard()
    # )

async def generate_vpn_settings(user_state):
    with session_maker() as session:
        user_data = await user_state.get_data()
        vpn: Vpn = session.query(Vpn).where(Vpn.user_id == user_data.get('id')).first()
        server = choose_server()
        ip = choose_ip(server)
        private_key = generate_key()
        pub_key = public_key(private_key)
        vpn.status = 'executed'
        vpn.server_id = server.id
        vpn.ip = ip
        vpn.public_key = pub_key
        vpn.updated_at = datetime.now()
        await user_state.update_data(
            vpn_status='executed'
        )
        with open(f'servers/{server.name}/{server.name}_peer.conf', 'r') as peer:
            peer_config = peer.read()
        with open(f'users/config/endurancevpn_{vpn.user_id}.conf', 'w') as config:
            config.write(
                '[Interface]\n'
                f'PrivateKey = {private_key}\n'
                f'Address = {ip}/32\n'
                'DNS = 8.8.8.8, 8.8.4.4, 1.1.1.1\n\n'
                f'{peer_config}'
            )
        session.add(vpn)
        session.commit()
        logger.info(f'Для пользователя id={vpn.user_id} сгенерированы настройки.')

def choose_server():
    """ Выбираем сервер для пользователя """
    with session_maker() as session:
        with session_maker() as session:
            servers = session.query(Server).all()
            user_cnt_dict = {}
            for server in servers:
                server_user_cnt = session.query(Vpn).where(Vpn.server_id == server.id).count()
                user_cnt_dict[server.id] = server_user_cnt
            server_id_with_min_user_cnt = min(user_cnt_dict, key=user_cnt_dict.get)
            server = session.query(Server).where(Server.id == server_id_with_min_user_cnt).first()
            return server

def choose_ip(server: Server):
    """ Генерируем IP, чтобы не совпадал с уже имеющимися"""
    with session_maker() as session:
        ip_list = [item.ip for item in session.query(Vpn.ip).filter(Vpn.server_id == server.id)]
        net = IPv4Network(server.lan_net)
        ip = str(net.random_ip())
        while ip in ip_list or ip == server.lan_ip:
            ip = str(net.random_ip())
        return ip

async def update_server_config(server: Server):
    """ Генерирует конфиг сервера с пользователями,
    исключая пользователей с истекшим сроком подписки """
    with session_maker() as session:
        users = session.query(User).filter(or_(
            User.status == 'subscribed',
            User.status == 'trial'
            )).all()
        with open(f'servers/{server.name}/{server.name}_wg0.conf', 'r') as file:
            text = file.read()
        for user in users:
            if user.vpn.status == 'executed' and user.vpn.server_id == server.id:
                text += f'\n#user_{user.id}\n'\
                        f'[Peer]\n'\
                        f'PublicKey = {user.vpn.public_key}\n'\
                        f'AllowedIPs = {user.vpn.ip}\n'
        with open(f'servers/{server.name}/wg0.conf', 'w') as conf:
            conf.write(text)