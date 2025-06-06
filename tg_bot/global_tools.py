from .base import BOT
import settings
from aiogram.dispatcher.filters import Filter
from aiogram.types import (
    CallbackQuery, ChatActions, InlineKeyboardMarkup, InputFile, InputMediaDocument, MediaGroup, Message,
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
)
from aiogram.utils import exceptions as aiogram_exceptions
from io import IOBase
import logging
from typing import Awaitable, Callable


class CallbackChecker(Filter):
    def __init__(self, checker: Callable[[CallbackQuery], Awaitable[bool]]):
        self.__checker = checker

    async def check(self, callback: CallbackQuery) -> bool:
        return await self.__checker(callback)


class MessageChecker(Filter):
    def __init__(self, checker: Callable[[Message], Awaitable[bool]]):
        self.__checker = checker

    async def check(self, message: Message) -> bool:
        return await self.__checker(message)


async def send_message_to_admins(text: str, kb: InlineKeyboardMarkup | None = None):
    for admin_tg_peer_id in settings.BOT_ADMIN_IDs:
        try:
            await BOT.send_message(chat_id=admin_tg_peer_id, parse_mode="HTML", text=text, reply_markup=kb)
        except (aiogram_exceptions.ChatNotFound, aiogram_exceptions.BotBlocked):
            logging.warning("Bot hasn't (or blocked by) 'BOT_DEVELOPER_TG_ID'!")


async def send_message(chat_id: int, text: str, kb: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | None = None):
    await ChatActions.typing()
    try:
        await BOT.send_message(chat_id=chat_id, parse_mode="HTML", text=text, reply_markup=kb)
    except (aiogram_exceptions.ChatNotFound, aiogram_exceptions.BotBlocked):
        pass


async def delete_message(message: Message):
    try:
        await message.delete()
    except (aiogram_exceptions.MessageToDeleteNotFound, aiogram_exceptions.MessageCantBeDeleted):
        pass


async def edit_callback(callback: CallbackQuery, text: str, kb: InlineKeyboardMarkup | None = None):
    try:
        if callback.message.text:
            await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=kb)
        else:
            await delete_message(callback.message)
            raise aiogram_exceptions.MessageNotModified(message="message doesn't contain text")
    except (aiogram_exceptions.MessageToEditNotFound, aiogram_exceptions.MessageNotModified):
        await callback.message.answer(text=text, parse_mode="HTML", reply_markup=kb, disable_notification=True)


async def edit_if_callback_reply_if_message(
        callback_or_message: CallbackQuery | Message, text: str, kb: InlineKeyboardMarkup | None = None
):
    if isinstance(callback_or_message, CallbackQuery):
        await edit_callback(callback=callback_or_message, text=text, kb=kb)
    elif isinstance(callback_or_message, Message):
        await callback_or_message.reply(text=text, reply_markup=kb, parse_mode="HTML")
    else:
        raise ValueError(f"Invalid value 'callback_or_message': {callback_or_message}")


async def send_documents(*docs_filepaths_or_bytesio: str | IOBase, chat_id: int, text: str | None = None, notify=True) -> list[Message]:
    await ChatActions.upload_document()
    media_group = [
        InputMediaDocument(media=InputFile(doc_filepath_or_bytesio))
        for doc_filepath_or_bytesio in docs_filepaths_or_bytesio[:-1]
    ]
    media_group.append(
        InputMediaDocument(media=InputFile(docs_filepaths_or_bytesio[-1]), caption=text, parse_mode="HTML")
    )
    return await BOT.send_media_group(
        chat_id=chat_id, media=MediaGroup(media_group), disable_notification=not notify,
    )
