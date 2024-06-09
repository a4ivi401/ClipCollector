from telebot import types
from utils.chat_ids import read_chat_ids, add_chat_id

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_message(message):
        chat_id = message.chat.id
        chat_ids = read_chat_ids()
        if chat_id not in chat_ids:
            add_chat_id(chat_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        yt_btn = types.KeyboardButton('📺YouTube')
        tt_btn = types.KeyboardButton('📺TikTok')
        pin_btn = types.KeyboardButton('📺Pinterest')
        faq_btn = types.KeyboardButton('❓FAQ')
        report_btn = types.KeyboardButton('📤Сообщить о проблеме')
        markup.add(yt_btn, tt_btn, pin_btn, faq_btn, report_btn)
        bot.send_message(message.chat.id, 'Привет! Я ClipCollectorBot и я умею скачивать видео с разных площадок. Выбери необходимую тебе и отправь мне видео! P.S Я нахожусь в стадии Закрытого Бета Теста, поэтому в случае возникновения пролемы прошу сообщить автору бота', reply_markup = markup)