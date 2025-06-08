from ..base import DP
from ..surveys.utils import start_survey
import database.tasks as db
import settings
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import Message, ContentType


WAIT_DEPARTMENT_STATE = State(state="WAIT_DEPARTMENT", group_name="StartBlock")


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
            parse_mode="HTML", text=(
                "Чтоб пользоваться ботом, Вы должны перейти по <u>специальной ссылке на опрос</u>"
                if message.from_user.id not in settings.BOT_ADMIN_IDs else
                "Доступные команды:\n\n/users - просмотр пользователей и результатов их опросов\n/surveys - пригласительные ссылки на прохождение опроса"
            ),
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
