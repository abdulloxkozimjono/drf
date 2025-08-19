import threading
import asyncio
from tg_bot.bot import start_bot


def run_bot():
    def bot_thread():
        asyncio.run(start_bot())

    thread = threading.Thread(target=bot_thread, name="TelegramBotThread", daemon=True)
    thread.start()
    print("thread bilan bot ishga tushdi")