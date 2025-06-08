from ..base import DP
from ..surveys.base import Surveys, FREE_ANSWER
from ..global_tools import send_message
import database.tasks as db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import Message, ContentType
import asyncio


WAIT_DEPARTMENT_STATE = State(state="WAIT_DEPARTMENT", group_name="StartBlock")


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


@DP.message_handler(state=WAIT_DEPARTMENT_STATE, content_types=ContentType.ANY)
async def get_department(message: Message, state: FSMContext):
    if not message.text:
        await message.reply("Ответить можно только текстовым сообщением\nНапишите, <b>в каком отделе Вы работаете</b>:")
        return
    db.user.write_user(tg_peer_id=message.from_user.id, full_name=message.from_user.full_name, department=message.text)
    await start_survey(
        user_tg_peer_id=message.from_user.id,
        survey_id=(await state.get_data())["survey_id"],
        state=state,
    )


@DP.message_handler(commands=["start"], state="*")
async def start(message: Message, state: FSMContext):
    try:
        survey_id = int(message.get_args())
    except ValueError:
        await message.answer(
            text="Чтоб пользоваться ботом, Вы должны перейти по <u>специальной ссылке на опрос</u>", parse_mode="HTML",
        )
        return
    if not db.user.is_user_exists(message.from_user.id):
        await message.answer(
            text=(
                f"Добро пожаловать, {message.from_user.full_name}!"
                "\nПрежде, чем мы начнём опрос, пожалуйста, напишите, <b>в каком отделе Вы работаете</b>:"
            ), parse_mode="HTML",
        )
        await WAIT_DEPARTMENT_STATE.set()
        await state.set_data({"survey_id": survey_id})
        return
    await start_survey(
        user_tg_peer_id=message.from_user.id,
        survey_id=survey_id,
        state=state,
    )
