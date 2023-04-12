from aiogram import types
from aiogram.dispatcher import FSMContext
from db.connect import session_maker
from db.models import User, Vpn, Server
from services.keys import generate_key, public_key
from datetime import datetime
from loader import logger
from subnet import IPv4Network
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
        vpn.status = 'requested'
        await state.update_data(
            vpn_status='requested'
        )
        session.add(vpn)
        session.commit()

def send_vpn_settings(user_data):
    pass

def generate_vpn_settings(user_data):
    with session_maker() as session:
        vpn: Vpn = session.query(Vpn).where(Vpn.user_id == user_data.get('id'))
        server = choose_server()
        ip = choose_ip(server)
        private_key = generate_key()
        pub_key = public_key(private_key)
        vpn.status = 'executed'
        vpn.server_id = server.id
        vpn.ip = ip
        vpn.public_key = pub_key
        vpn.updated_at = datetime.now()



def choose_server():
    """ Выбираем сервер для пользователя """
    with session_maker() as session:
        servers = session.query(Server).all()
        for server in servers:
            users_cnt = session.query(Vpn).where(Vpn.server_id == server.id).count()
            print(users_cnt)
            if users_cnt < settings.MAX_SERVER_USER_COUNT:                       
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

# def generate_user_config(user: User):
#     """ Генерируется конфиг для пользователя """
#     logger.info(
#         f'Получен запрос на генерацию конфига от пользователя {user.name}, ID {user.id}'
#         )
#     server: Server = choose_server()
#     server.users_cnt += 1
#     user_ip = choose_ip(server)
#     priv_key = generate_key()
#     pub_key = public_key(priv_key)
#     create_vpn(user, server, user_ip, pub_key)
#     user.vpn_status = 'pending'
#     user.updated_at = datetime.now()
#     with open(f'servers/instance/{server.name}_peer.txt', 'r') as peer:
#         peer_config = peer.read()
#         with open(f'users/config/{user.id}.conf', 'w') as cfg:
#             cfg.write(
#                 '[Interface]\n'
#                 f'PrivateKey = {priv_key}\n'
#                 f'Address = {user_ip}/32\n'
#                 'DNS = 8.8.8.8\n\n'
#                 f'{peer_config}'
#             )
#     logger.info(f'Конфигурация для пользователя ID {user.id} сгенерирована.')
#     subprocess.run(
#         f'qrencode -t png -o users/qr/{user.id}.png < users/config/{user.id}.conf',
#         shell=True
#         )
#     logger.info(f'QR код для пользователя ID {user.id} сгенерирован.')
#     update_item(server)
#     update_item(user)