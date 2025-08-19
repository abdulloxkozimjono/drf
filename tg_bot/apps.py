import os
from django.apps import AppConfig

class TgBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tg_bot'

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":
            print("Bot ready() dan chaqirildi")
            from tg_bot.runer_bot import run_bot
            run_bot()