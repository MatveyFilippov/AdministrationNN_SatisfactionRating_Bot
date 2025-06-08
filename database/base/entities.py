from .properties import Base, ENGINE
import settings
from datetime import datetime
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint


class User(Base):
    __tablename__ = "users"

    tg_peer_id = Column(sqlalchemy.BigInteger, primary_key=True)
    full_name = Column(sqlalchemy.Text, nullable=False)
    department = Column(sqlalchemy.Text, nullable=False)
    registered_at = Column(sqlalchemy.DateTime(True), nullable=False, default=lambda: datetime.now(settings.BOT_TIMEZONE))

    @property
    def bot_link_to_user(self):
        return f"tg://user?id={self.tg_peer_id}"


class Survey(Base):
    __tablename__ = "surveys"

    # BigInteger doesn't work with auto-increment in SQLite
    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.Text, nullable=False)
    respondent_tg_peer_id = Column(
        sqlalchemy.BigInteger, ForeignKey(
            "users.tg_peer_id", onupdate="CASCADE", ondelete="CASCADE",
        ), nullable=False,
    )
    start_at = Column(sqlalchemy.DateTime(True), nullable=False, default=lambda: datetime.now(settings.BOT_TIMEZONE))

    __table_args__ = (
        Index('idx_respondent', 'respondent_tg_peer_id'),
    )


class QuestionAnswer(Base):
    __tablename__ = "questions_answers"

    survey_id = Column(
        sqlalchemy.Integer, ForeignKey(
            "surveys.id", onupdate="CASCADE", ondelete="CASCADE",
        ), nullable=False, primary_key=True,
    )
    local_number = Column(sqlalchemy.Integer, nullable=False)
    question = Column(sqlalchemy.Text, nullable=False, primary_key=True)
    answer = Column(sqlalchemy.Text, nullable=False)

    __table_args__ = (
        Index("idx_survey", "survey_id"),
        UniqueConstraint("survey_id", "local_number", name="uq_survey_question_number"),
    )


Base.metadata.create_all(ENGINE)
