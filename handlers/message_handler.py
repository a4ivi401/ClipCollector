import yt_dlp
from tiktok_downloader import ttdownloader
from utils.logging import log_error
import os
from utils.random_filename import uuid_filename
from utils import pinterest

def register_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            if message.text == '📺YouTube' or message.text == 'YouTube':
                bot.send_message(message.chat.id, "Отправь мне ссылку на видео Youtube")
            elif message.text == '📺TikTok' or message.text == 'TikTok':
                bot.send_message(message.chat.id, "Отправь мне ссылку на клип TikTok")
            elif message.text == '📺Pinterest' or message.text == 'Pinterest':
                bot.send_message(message.chat.id, "Отправь мне ссылку на клип TikTok")
            elif message.text == '❓FAQ' or message.text == 'FAQ':
                with open('faq.txt', 'r') as file:
                    text = file.read()
                    bot.send_message(message.chat.id, text)
            elif message.text == '📤Сообщить о проблеме' or message.text == 'Сообщить о проблеме':
                bot.send_message(message.chat.id, "Если у вас возникла проблема, прошу сообщить об этом автору бота: @a4ivi4")
            elif 'youtube.com' in message.text or 'youtu.be' in message.text:
                url = message.text
                ytfilename = uuid_filename + '.mp4'
                if 'youtube.com' in url or 'youtu.be' in url:
                    ydl_opts = {
                        'format': 'bestvideo[ext=mp4][vcodec=h264]+bestaudio[ext=m4a]/best[ext=mp4][vcodec=h264]/best[ext=mp4]/best',
                        'outtmpl': ytfilename,
                    }
                    try:
                        url_allow = url
                        bot.send_chat_action(message.chat.id, 'upload_video')
                        ydl = yt_dlp.YoutubeDL(ydl_opts)
                        info = ydl.extract_info(url_allow, download=True)
                        with open(ytfilename, "rb") as file:
                            bot.send_video(message.chat.id, file, timeout=240)
                        bot.reply_to(message, 'Видео успешно скачано')
                        os.remove(ytfilename)

                    except Exception as e:
                        bot.reply_to(message, f'Произошла ошибка при скачивании видео: {e}')
                        os.remove(ytfilename)
                else:
                    bot.reply_to(message, 'Ссылка не поддерживается. Пожалуйста, повторите попытку')
            elif 'tiktok.com' in message.text:
                url = message.text
                filename = uuid_filename + '.mp4'
                if 'tiktok.com' in url:
                    try:
                        bot.send_chat_action(message.chat.id, 'upload_video')
                        d = ttdownloader(url)
                        d[0].download(filename)
                        with open(filename, 'rb') as file:
                            bot.send_video(message.chat.id, file)
                        bot.reply_to(message, 'Видео из TikTok успешно скачано')
                        os.remove(filename)
                    except Exception as e:
                        bot.reply_to(message, 'Произошла ошибка при скачивании видео')
                        print(e)
                        os.remove(filename)
                else:
                    bot.reply_to(message, 'Ссылка не поддерживается. Пожалуйста, повторите попытку')
            elif 'pinterest.com' in message.text or 'pin.it' in message.text:
                try:
                    url = message.text
                    pinvideo_filename = uuid_filename + '.mp4'
                    bot.send_chat_action(message.chat.id, 'upload_video')
                    pinterest_video = pinterest.PinterestVideo(url)
                    video_url = pinterest_video.get_video_url()
                    with open(pinvideo_filename, 'wb') as file:
                        file.write(video_url.content)
                    with open(pinvideo_filename, 'rb') as file:
                        bot.send_video(message.chat.id, file)
                    bot.reply_to(message, 'Видео из Pinterest успешно скачано.')
                    os.remove(pinvideo_filename)
                except Exception as e:
                    log_error(e)
                    bot.reply_to(message, 'Произошла ошибка при скачивании видео')
        except Exception as e:
            log_error(e)
            bot.reply_to(message, f'Произошла ошибка при скачивании видео')