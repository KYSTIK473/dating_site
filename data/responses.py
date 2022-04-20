import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Responses(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "responses"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_person = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True
    )
    id_person_responses = sqlalchemy.Column(
        sqlalchemy.String, nullable=True, default=None
    )
    id_responses_to_person = sqlalchemy.Column(
        sqlalchemy.String, nullable=True, default=None
    )
    vz_responses = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    user = orm.relation("User")
