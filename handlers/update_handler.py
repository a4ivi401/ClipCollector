from telebot import types
import config

def register_handlers(bot):
    @bot.message_handler(commands=['info_update'])
    def info_update(message):
        if message.chat.id == config.ADMIN_CHAT_ID:
            for i in open('chatids.txt', 'r').readlines():
                with open('update_list.txt', 'r') as file:
                    text = file.read()
                    bot.send_message(i, text)