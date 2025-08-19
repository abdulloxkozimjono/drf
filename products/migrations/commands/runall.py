# import os
# import asyncio
# from django.core.management import execute_from_command_line
# from bot.telegram_bot import main
#
# asyncio.run(main())
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
#
#
# # Django serverni ishga tushurish
# async def main():
#     # Django serverni alohida processda ishga tushirish
#     from threading import Thread
#     def run_django():
#         execute_from_command_line(['manage.py', 'runserver'])
#
#     django_thread = Thread(target=run_django)
#     django_thread.start()
#
#     # Telegram botni ishga tushirish
#     await start_bot()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
# #