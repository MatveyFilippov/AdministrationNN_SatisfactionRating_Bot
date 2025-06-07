from ..base.properties import Session
from ..base.entities import User


def _get_user(session: Session, tg_peer_id: int, raise_error_if_not_exists=False) -> User | None:
    user = session.get(User, tg_peer_id)
    if raise_error_if_not_exists and not user:
        raise KeyError(f"No such user in database with TG PEER ID: {tg_peer_id}")
    return user


def write_or_rewrite_user(tg_peer_id: int, full_name: str):
    with Session() as session:
        user = _get_user(session, tg_peer_id)
        if user and user.full_name != full_name:
            user.full_name = full_name
            session.commit()
        elif not user:
            session.add(User(tg_peer_id=tg_peer_id, full_name=full_name))
            session.commit()


def get_user(tg_peer_id: int, raise_error_if_not_exists=True) -> User | None:
    with Session() as session:
        return _get_user(session=session, tg_peer_id=tg_peer_id, raise_error_if_not_exists=raise_error_if_not_exists)


def get_all_users() -> list[User]:
    with Session() as session:
        return session.query(User).order_by(User.registered_at.asc()).all()
