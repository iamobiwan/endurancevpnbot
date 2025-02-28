from sqlalchemy.orm import relationship
import sqlalchemy as sql
from .connect import Base


class User(Base):
    __tablename__ = 'user'

    id = sql.Column(sql.Integer, primary_key=True)
    telegram_id = sql.Column(sql.BigInteger, nullable=False)
    chat_id = sql.Column(sql.BigInteger, nullable=False)
    name = sql.Column(sql.String(50))
    status = sql.Column(sql.String(10), default='created')
    promocode = sql.Column(sql.String(10), nullable=True)
    discount = sql.Column(sql.Integer(), default=0)
    inviting_user_id = sql.Column(sql.Integer(), nullable=True)
    created_at = sql.Column(sql.DateTime)
    updated_at = sql.Column(sql.DateTime)
    expires_at = sql.Column(sql.DateTime, nullable=True)
    vpn = relationship('Vpn', uselist=False, back_populates='user')
    order = relationship('Order', backref='user')


class Server(Base):
    __tablename__ = 'server'

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(30))
    lan_net = sql.Column(sql.String(18))
    lan_ip = sql.Column(sql.String(18))
    wan_ip = sql.Column(sql.String(15))

    vpn = relationship('Vpn', backref='server')

    def __repr__(self) -> str:
        return f'{self.name}'
    

class Vpn(Base):
    __tablename__ = 'vpn'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    status=sql.Column(sql.String(10), default='created')
    server_id = sql.Column(sql.Integer, sql.ForeignKey('server.id', ondelete='cascade'))
    ip = sql.Column(sql.String(18))
    public_key = sql.Column(sql.String(50))
    created_at = sql.Column(sql.DateTime)
    updated_at = sql.Column(sql.DateTime)
    user = relationship('User', back_populates='vpn')


class Plan(Base):
    __tablename__ = 'plan'

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(30))
    days = sql.Column(sql.Integer)
    amount = sql.Column(sql.Integer)


class Order(Base):
    __tablename__ = 'order'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'))
    status = sql.Column(sql.String(10))
    amount = sql.Column(sql.Integer)
    label = sql.Column(sql.String(25))
    days = sql.Column(sql.Integer)
    donate_url = sql.Column(sql.String(200), nullable=True)
    invite_discount = sql.Column(sql.Boolean, default=False)
    deleted = sql.Column(sql.Boolean, default=False)
    created_at = sql.Column(sql.DateTime)
    updated_at = sql.Column(sql.DateTime)