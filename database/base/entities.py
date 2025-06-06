from .properties import Base, ENGINE
import settings
from datetime import datetime
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Index


class User(Base):
    __tablename__ = "users"

    tg_peer_id = Column(sqlalchemy.BigInteger, primary_key=True)
    full_name = Column(sqlalchemy.Text, nullable=False)
    registered_at = Column(sqlalchemy.DateTime(True), nullable=False, default=lambda: datetime.now(settings.BOT_TIMEZONE))

    @property
    def bot_link_to_user(self):
        return f"tg://user?id={self.tg_peer_id}"


Base.metadata.create_all(ENGINE)
