def start():
    from .branches import register_all
    register_all()
    from aiogram.utils import executor
    from .misc import on_startup, on_shutdown
    from .base import DP
    executor.start_polling(DP, on_startup=on_startup, on_shutdown=on_shutdown)
