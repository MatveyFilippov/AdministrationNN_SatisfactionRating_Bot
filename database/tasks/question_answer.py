from ..base.properties import Session
from ..base.entities import QuestionAnswer


def append_question_answer(survey_id: int, question: str, local_number: int, answer: str):
    with Session() as session:
        session.add(QuestionAnswer(
            survey_id=survey_id,
            question=question,
            local_number=local_number,
            answer=answer,
        ))
        session.commit()


def is_has_answer(survey_id: int, question: str):
    with Session() as session:
        return session.get(QuestionAnswer, (survey_id, question)) is not None


def get_survey_questions_answers(survey_id: int) -> list[QuestionAnswer]:
    with Session() as session:
        return (
            session.query(QuestionAnswer)
            .filter(QuestionAnswer.survey_id == survey_id)
            .order_by(QuestionAnswer.local_number.asc())
            .all()
        )
