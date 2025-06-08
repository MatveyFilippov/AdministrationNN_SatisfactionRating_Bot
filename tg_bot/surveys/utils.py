from .base import Surveys, FREE_ANSWER
from ..global_tools import send_message
import database.tasks as db
import settings
from aiogram.dispatcher import FSMContext
import asyncio
import csv
import io


async def start_survey(user_tg_peer_id: int, survey_id: int, state: FSMContext):
    survey = Surveys.get(survey_id)
    survey_id = db.survey.create_survey(
        name=survey.name,
        respondent_tg_peer_id=user_tg_peer_id,
    )
    await send_message(chat_id=user_tg_peer_id, text=(
        f"Вам предлагается пройти опрос '<b>{survey.name}</b>'\n\nВыбирайте ответы из предложенных вариантов."
        f"\nЕсли выбираете '<code>{FREE_ANSWER}</code>' - будьте готовы написать ответ самостоятельно."
        f"\nВ вопросах, где допустим множественный выбор, также обязательно предлагается '<code>{FREE_ANSWER}</code>', "
        f"Вы в праве выбрать '<code>{FREE_ANSWER}</code>' и перечислить несколько вариантов."
        "\n\n<b>Будьте искренне и осторожны, отменить ответ нельзя!</b>"
    ))
    await asyncio.sleep(3.5)
    await survey.first_question.send(user_tg_peer_id)
    await state.set_data({"survey_id": survey_id})


def get_survey_csv_bytesio(survey_id: int) -> io.IOBase:
    csv_buffer = io.StringIO()

    fieldnames = ["question", "answer"]
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()

    for question_answer in db.question_answer.get_survey_questions_answers(survey_id):
        writer.writerow({
            "Вопрос": question_answer.question,
            "Ответ": question_answer.answer,
        })

    csv_buffer.seek(0)

    bytes_io = io.BytesIO(csv_buffer.getvalue().encode("utf-8"))
    bytes_io.seek(0)
    bytes_io.name = f"Survey_{survey_id}.csv"
    return bytes_io


def get_survey_description(survey_id: int) -> str:
    survey = db.survey.get_survey(survey_id)
    user = db.user.get_user(survey.respondent_tg_peer_id)
    return (
        f"<u>Опрос</u>:\n'{survey.name}'\n\n<u>Дата начала</u>:"
        f"\n{survey.start_at.strftime(settings.DATETIME_FORMAT)} ({settings.BOT_TIMEZONE.zone})"
        f"\n\n<u>Респондент</u>:\n<a href='{user.bot_link_to_user}'>{user.full_name}</a> ({user.department})"
        f"\n\n<u>ID</u>:\n<code>{survey.id}</code>"
    )
