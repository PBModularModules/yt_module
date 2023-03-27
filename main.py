from pytube import YouTube
from base.module import command, BaseModule
import os
import re
from pyrogram.types import Message

class YoutubeModule(BaseModule):
    @command('yt')
    async def yt_cmd(self, _, message: Message):
        err = self.S["download"]["error"]
        caption = self.S["download"]["ok"]
        no_url = self.S["etc"]["no_url"]
        process = self.S["etc"]["process"]
        not_url = self.S["etc"]["not_url"]
        try:
            # Получаем ссылку на видео из аргументов команды
            args = message.text.split()
            if len(args) < 2:
                # Отправляем сообщение о необходимости указать ссылку на видео
                await message.reply(no_url)
                return
            url = args[1]
            
            # Проверяем, является ли переданный аргумент ссылкой на видео на YouTube
            match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
            if not match:
                # Отправляем сообщение об ошибке
                await message.reply(not_url)
                return

            # Создаем объект YouTube и передаем ссылку на видео в качестве аргумента
            yt = YouTube(url)

            # Задаем имя файла для его удаления
            fn = yt.title

            # Получаем лучшее качество видео и загружаем его во временную папку
            video = yt.streams.get_highest_resolution()
            video_path = video.download(output_path="/tmp", filename=f'{fn}.mp4')
            await message.reply(process)

            # Отправляем загруженное видео в чат с подписью
            await message.reply_video(video_path, caption=caption)

            # Удаляем файл дабы не засорять внутренне хранилище
            os.remove(f'/tmp/{fn}.mp4')

        except Exception as e:
            # Отправляем сообщение об ошибке в чат
            await message.reply(f"{err} <b>{str(e)}</b>")
