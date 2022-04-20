import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Room(SqlAlchemyBase):
    __tablename__ = "rooms"
    id_room = sqlalchemy.Column(
        sqlalchemy.String,  primary_key=True)
