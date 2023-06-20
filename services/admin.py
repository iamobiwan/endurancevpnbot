from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main import start_main
from db.connect import session_maker
from loader import logger, config, dp
from misc import messages
from datetime import datetime, timedelta
from services.user import get_user
from db.models import User, Vpn, Server
from sqlalchemy import func, desc, or_, and_
import settings


async def extend_user_sub(edit_user_id, sub_days):
    with session_maker() as session:
        user: User = session.query(User).filter(User.id == edit_user_id).first()
        user_state: FSMContext = dp.current_state(user=user.telegram_id, chat=user.chat_id)
        if user.status in ['subscribed', 'trial']:
            user.expires_at = user.expires_at + timedelta(days=sub_days)
        elif user.status in ['expired', 'outdated']:
            user.expires_at = datetime.now() + timedelta(days=sub_days)
        user.status = 'subscribed'
        await user_state.update_data(
            status=user.status,
            expires_at=user.expires_at.strftime("%d.%m.%Y")
        )
        session.add(user)
        session.commit()
            
async def reset_user_vpn(user_id):
    with session_maker() as session:
        user: User = session.query(User).filter(User.id == user_id).first()
        user_state: FSMContext = dp.current_state(user=user.telegram_id, chat=user.chat_id)
        await user_state.update_data(vpn_status='created')
        user.vpn.status = 'created'
        user.vpn.server_id = None
        user.vpn.ip = None
        user.vpn.public_key = None
        user.vpn.updated_at = datetime.now()
        session.add(user)
        session.commit()

async def end_user_sub(edit_user_id):
    pass

async def set_discount(user_id, discount):
    with session_maker() as session:
        user: User = session.query(User).filter(User.id == user_id).first()
        user.discount = discount
        session.add(user)
        session.commit()

def test():
    pass
    # with session_maker() as session:
    #     servers = session.query(Server).all()
    #     user_cnt_dict = {}
    #     for server in servers:
    #         server_user_cnt = session.query(Vpn).where(Vpn.server_id == server.id).count()
    #         user_cnt_dict[server.id] = server_user_cnt
        
    #     server_id_with_min_user_cnt = min(user_cnt_dict, key=user_cnt_dict.get)
    #     server = session.query(Server).where(Server.id == server_id_with_min_user_cnt).first()
    #     vpns = session.query(Vpn).filter(Vpn.server_id == server.id)
        # for vpn in vpns:
        #     if vpn.status
        # # users = session.query(User).filter(or_(
        # #     User.status == 'subscribed',
        # #     User.status == 'trial'
        # #     )).all()
        # users = session.query(User).filter(User.vpn.server_id == server.id).all()
        # print(users)

