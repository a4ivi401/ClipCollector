import logging
from telebot import TeleBot
from handlers import start_handler, update_handler, message_handler
import config

logging.basicConfig(filename='bot.log', level=logging.ERROR)

bot = TeleBot(config.BOT_TOKEN)

start_handler.register_handlers(bot)
update_handler.register_handlers(bot)
message_handler.register_handlers(bot)

bot.polling(non_stop=True, timeout=240)