from .base import BOT, DP
from .global_tools import CallbackChecker, delete_message, send_message_to_admins
import settings
from aiogram.types import CallbackQuery, ContentType, Message, Update
from aiogram.utils import exceptions as aiogram_exceptions
from datetime import datetime
import logging
import traceback


async def on_startup(dispatcher):
    await send_message_to_admins("Бот был отключен -> работает 🐥")
    print("Bot is alive")


async def on_shutdown(dispatcher):
    logging.info("Bot is shut down")
    await send_message_to_admins("⚠️<b>Бот выключен</b>⚠️")


@DP.edited_message_handler(state="*")
async def handle_edited_message(message: Message):
    await message.reply("""🚫Вы внесли изменения, а, к сожалению, в нашем боте <b>НЕ ПРЕДУСМОТРЕНА</b> такая функция(
    \nПолучатель <b>НЕ УВИДИТ</b> ваших изменений. 💬Лучше отправьте ещё одно сообщение""", parse_mode="HTML")


@DP.callback_query_handler(CallbackChecker(lambda c: c.data.startswith("delete_message")), state="*")
async def delete_message(callback: CallbackQuery):
    if callback.data.endswith("+1"):
        try:
            await delete_message(callback.message.reply_to_message.message_id)
        except AttributeError:
            pass
    await delete_message(callback.message)


@DP.callback_query_handler(state="*")
async def unknown_callback(callback: CallbackQuery):
    if callback.data.startswith("TODO"):
        await callback.answer("👷\nДанный раздел находится в разработке", show_alert=True)
        return
    await callback.answer(f"🤷\nНеизвестная кнопка: {callback.data} ", show_alert=True)


@DP.message_handler(content_types=ContentType.ANY, state="*")
async def another_message(message: Message):
    await message.reply(text="Извините, я не понял ваш запрос 😔", parse_mode="HTML")


@DP.errors_handler()
async def error_handler(update: Update, exception: Exception):
    err_time = datetime.now(settings.BOT_TIMEZONE).strftime(settings.DATETIME_FORMAT)
    error_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    tb = traceback.extract_tb(exception.__traceback__)
    logging.error(f"{type(exception).__name__} in '{tb[-1].name}'", exc_info=True)
    try:
        await BOT.send_message(
            chat_id=update.message.chat.id, parse_mode="HTML", disable_notification=True,
            text=(
                f"{err_time} ({settings.BOT_TIMEZONE.zone}) --- <b>ERROR</b>"
                "\nПередал информацию об ошибке разработчикам, попробуйте позже"
            ),
        )
        if update.message.from_user.username:
            text = f"Ошибка от @{update.message.from_user.username}"
        else:
            text = f"Ошибка от {update.message.from_user.full_name}"
    except AttributeError:
        text = "Ошибка в самом коде"
    except (aiogram_exceptions.ChatNotFound, aiogram_exceptions.BotBlocked):
        text = "Ошибка от пользователя, который перестал пользоваться ботом"

    await send_message_to_admins((
        f"{err_time} ({settings.BOT_TIMEZONE.zone})"
        f"\nПроизошла ошибка <b>{type(exception).__name__}</b> в функции {tb[-1].name}"
    ))
    await send_message_to_admins(text + f"\n\n<code>{error_text}</code>")
