from ..base.properties import Session
from ..base.entities import Survey


def _get_survey(session: Session, survey_id: int, raise_error_if_not_exists=False) -> Survey | None:
    survey = session.get(Survey, survey_id)
    if raise_error_if_not_exists and not survey:
        raise KeyError(f"No such survey in database with ID: {survey_id}")
    return survey


def create_survey(name: str, respondent_tg_peer_id: int) -> int:
    with Session() as session:
        new_survey = Survey(
            name=name,
            respondent_tg_peer_id=respondent_tg_peer_id,
        )
        session.add(new_survey)
        session.commit()
        return new_survey.id


def get_user_surveys(tg_peer_id: int) -> list[Survey]:
    with Session() as session:
        return (
            session.query(Survey)
            .filter(Survey.respondent_tg_peer_id == tg_peer_id)
            .order_by(Survey.start_at.asc())
            .all()
        )


def get_survey(survey_id: int, raise_error_if_not_exists=True) -> Survey | None:
    with Session() as session:
        return _get_survey(session=session, survey_id=survey_id, raise_error_if_not_exists=raise_error_if_not_exists)
