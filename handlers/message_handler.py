import yt_dlp
from tiktok_downloader import ttdownloader
from utils.logging import log_error
import os
from utils.random_filename import uuid_filename
import requests
from bs4 import BeautifulSoup
from utils.pinterest import download_pin
import re

def register_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            if message.text == '📺YouTube' or message.text == 'YouTube':
                bot.send_message(message.chat.id, "Отправь мне ссылку на видео Youtube")
            elif message.text == '📺TikTok' or message.text == 'TikTok':
                bot.send_message(message.chat.id, "Отправь мне ссылку на клип TikTok")
            elif message.text == '📺Pinterest' or message.text == 'Pinterest':
                bot.send_message(message.chat.id, "Отправь мне ссылку на видео Pinterest")
            elif message.text == '📺Pinterest GIF' or message.text == 'Pinterest GIF':
                gif = bot.send_message(message.chat.id, "Отправь мне ссылку на GIF Pinterest")
                bot.register_next_step_handler(gif, download_pinterest_gif)
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
                        bot.reply_to(message, 'Видео из YouTube успешно скачано')
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
            elif 'pin.it' in message.text:
                try:
                    url = message.text
                    bot.send_chat_action(message.chat.id, 'upload_video')
                    if("https://pin.it/" in url): 
                        t_body = requests.get(url)
                        if(t_body.status_code!= 200):
                            bot.reply_to(message, "Введенный URL недействителен или не работает")
                            return
                        soup = BeautifulSoup(t_body.content,"html.parser")
                        href_link = (soup.find("link",rel="alternate"))['href']
                        match = re.search('url=(.*?)&', href_link)
                        url = match.group(1) 
                    body = requests.get(url) 
                    if(body.status_code!= 200): 
                        bot.reply_to(message, "Введенный URL недействителен или не работает")
                        return
                    soup = BeautifulSoup(body.content, "html.parser") 
                    extract_url = (soup.find("video",class_="hwa kVc MIw L4E"))['src'] 
                    convert_url = extract_url.replace("hls","720p").replace("m3u8","mp4")
                    filename = uuid_filename +".mp4"
                    download_pin(convert_url, filename)
                    with open(filename, 'rb') as file:
                        bot.send_video(message.chat.id, file)
                    bot.reply_to(message, 'Видео из Pinterest успешно скачано')
                    os.remove(filename)
                except Exception as e:
                    log_error(e)
                    bot.reply_to(message, 'Произошла ошибка при скачивании видео')
        except Exception as e:
            log_error(e)
            bot.reply_to(message, f'Произошла ошибка при скачивании видео')
    
    def download_pinterest_gif(message):
        pinterest_url = message.text
        response = requests.get(pinterest_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        gifs = soup.find_all('video')
        media_files = []
        for img in images:
            img_url = img.get('src')
            if img_url:
                media_files.append(img_url)
        for gif in gifs:
            gif_url = gif.get('src')
            if gif_url:
                media_files.append(gif_url)
        for file in media_files:
            response = requests.get(file, stream=True)
            file_name = os.path.basename(file)
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            bot.send_document(message.chat.id, open(file_name, 'rb'))