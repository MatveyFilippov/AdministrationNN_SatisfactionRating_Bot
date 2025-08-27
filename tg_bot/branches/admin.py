from ..base import DP
from ..global_tools import CallbackChecker, edit_callback, edit_if_callback_reply_if_message, send_documents
from ..surveys import Surveys
from ..surveys.utils import get_survey_description, get_survey_csv_bytesio
import database.tasks as db
import settings
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from functools import lru_cache


ALL_SURVEYS_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=survey_obj.name, callback_data=f"survey_info:{survey_obj.survey_id}")]
    for survey_obj in Surveys.get_all()
])
BACK_TO_ALL_SURVEYS_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="🔙 Назад", callback_data="surveys")]
])


@DP.message_handler(commands=["surveys"], state="*")
@DP.callback_query_handler(text="surveys", state="*")
async def surveys(message_or_callback: Message | CallbackQuery, state: FSMContext):
    if message_or_callback.from_user.id not in settings.BOT_ADMIN_IDs:
        msg_to_answer = message_or_callback if isinstance(message_or_callback, Message) else message_or_callback.message
        await msg_to_answer.answer(
            "🤐 К сожалению, данное действие вам <b>не доступно</n>, так как вы <b>не являетесь администратором</b>",
            parse_mode="HTML"
        )
        return
    await state.finish()
    await edit_if_callback_reply_if_message(
        callback_or_message=message_or_callback, text="Список всех опросов:", kb=ALL_SURVEYS_INLINE_KEYBOARD,
    )


@DP.callback_query_handler(CallbackChecker(lambda c: c.data.startswith("survey_info:")), state="*")
async def survey_info(callback: CallbackQuery):
    survey_id = int(callback.data.removeprefix("survey_info:"))
    survey_obj = Surveys.get(survey_id)
    link_to_survey = await survey_obj.link_to_start
    text = f"""<b>{survey_obj.name}</b>\nСсылка на прохождение опрос:
    \n<code>{link_to_survey}</code>
    \nНажать на ссылку, чтоб скопировать её.
    """
    await edit_callback(callback=callback, text=text, kb=BACK_TO_ALL_SURVEYS_INLINE_KEYBOARD)


@lru_cache
def __get_users_page_borders(users_in_list: int, users_qty: int, page_index: int) -> tuple[int, int]:
    available_lists = users_qty / users_in_list
    if available_lists - int(available_lists) > 0:
        available_lists = int(available_lists)
    else:
        available_lists = int(available_lists) - 1

    if page_index < 0:
        page_index = available_lists
    elif page_index > available_lists:
        page_index = 0

    first = users_in_list * page_index
    last = first + users_in_list
    if last > users_qty:
        last = users_qty

    return first, last


def get_users_page_kb(page: int) -> InlineKeyboardMarkup:
    users_in_list = 6
    users_in_line = 2

    users_list = db.user.get_all_users()

    first_user_index, last_user_index = __get_users_page_borders(
        users_in_list=users_in_list, users_qty=len(users_list), page_index=page,
    )

    kb_btns = [
        [
            InlineKeyboardButton(
                text=user.full_name,
                callback_data=f"look_user:{user.tg_peer_id}?{page}"
            ) for user in users_list[user_index:user_index + users_in_line]
        ] for user_index in range(first_user_index, last_user_index, users_in_line)
    ]

    kb_btns.append(
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"users:{page - 1}"),
            InlineKeyboardButton(text="➡️", callback_data=f"users:{page + 1}"),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=kb_btns)


@DP.message_handler(commands=["users"], state="*")
@DP.callback_query_handler(CallbackChecker(lambda c: c.data.startswith("users:")), state="*")
async def users(message_or_callback: Message | CallbackQuery, state: FSMContext):
    if message_or_callback.from_user.id not in settings.BOT_ADMIN_IDs:
        msg_to_answer = message_or_callback if isinstance(message_or_callback, Message) else message_or_callback.message
        await msg_to_answer.answer(
            "🤐 К сожалению, данное действие вам <b>не доступно</n>, так как вы <b>не являетесь администратором</b>",
            parse_mode="HTML"
        )
        return

    await state.finish()
    try:
        page = int(message_or_callback.data.removeprefix("users:"))
    except (ValueError, AttributeError):
        page = 0
    await edit_if_callback_reply_if_message(
        message_or_callback, kb=get_users_page_kb(page),
        text="Привет, <b>Admin</b>\nНиже представлены все пользователи бота:",
    )


@DP.callback_query_handler(CallbackChecker(lambda c: c.data.startswith("look_user:")), state="*")
async def look_user(callback: CallbackQuery):
    data = callback.data.removeprefix("look_user:").split("?")
    user_tg_peer_id, user_page = int(data[0]), int(data[1])
    user = db.user.get_user(user_tg_peer_id, True)
    all_surveys = db.survey.get_user_surveys(user_tg_peer_id)
    all_surveys.reverse()
    try:
        last_survey = all_surveys[0]
        last_survey_date_str = f"{last_survey.start_at.strftime(settings.DATETIME_FORMAT)} ({settings.BOT_TIMEZONE_ABBREVIATION})"
    except IndexError:
        last_survey_date_str = "Ещё не проходил(а)"

    text = f"""<a href='{user.bot_link_to_user}'>{user.full_name}</a>
    \n<u>Дата регистрации</u>:\n{user.registered_at.strftime(settings.DATETIME_FORMAT)} ({settings.BOT_TIMEZONE_ABBREVIATION})
    \n<u>Отдел</u>: {user.department}
    \n<u>Всего пройдено опросов</u>: {len(all_surveys)}
    \n<u>Дата прохождения последнего опроса</u>:\n{last_survey_date_str}
    \nTG PEER ID (also ID in db): <code>{user_tg_peer_id}</code>
    """
    kb = [
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data=f"users:{user_page}"),
            InlineKeyboardButton(text=user.full_name, url=user.bot_link_to_user),
        ],
    ]
    kb.extend(
        [
            InlineKeyboardButton(text=survey.name, callback_data=f"get_survey:{survey.id}")
        ] for survey in all_surveys
    )
    await edit_callback(callback=callback, kb=InlineKeyboardMarkup(inline_keyboard=kb), text=text)


@DP.callback_query_handler(CallbackChecker(lambda c: c.data.startswith("get_survey:")), state="*")
async def get_user_profile(callback: CallbackQuery):
    survey_id = int(callback.data.removeprefix("get_survey:"))
    await send_documents(
        get_survey_csv_bytesio(survey_id), chat_id=callback.from_user.id, text=get_survey_description(survey_id),
    )
