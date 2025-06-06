import settings
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import User


BOT = Bot(settings.BOT_API_TOKEN)
DP = Dispatcher(BOT, storage=MemoryStorage())
__bot_info: User = None


async def get_bot_info() -> User:
    global __bot_info
    if __bot_info is None:
        __bot_info = await BOT.get_me()
    return __bot_info
