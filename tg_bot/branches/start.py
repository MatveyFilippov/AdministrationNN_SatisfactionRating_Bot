from ..base import DP
import database.tasks as db
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


@DP.message_handler(commands=["start"], state="*")
async def send_welcome(message: Message, state: FSMContext):
    await state.finish()
    db.user.write_or_rewrite_user(tg_peer_id=message.from_user.id, full_name=message.from_user.full_name)
    await message.answer(
        text=(
            f"<b>Добро пожаловать, {message.from_user.full_name}!</b>"
            "\nTODO: <code>НАПИСАТЬ_ТЕКСТ</code>"
        ), parse_mode="HTML",
    )
