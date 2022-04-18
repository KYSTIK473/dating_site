import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Msg(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "messages"
    id_first = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True
    )
    id_second = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True
    )
    message = sqlalchemy.Column(
        sqlalchemy.String, nullable=True, default='',  primary_key=True
    )
