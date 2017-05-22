# -*- coding: utf-8 -*-

import telebot
import time
import config
import os

bot = telebot.TeleBot(token=config.token)

@bot.message_handler(commands=['init'])  # means you type '/test'
def find_file_ids(message):
    for file in os.listdir('emotes/'):
        if file.split('.')[-1] == 'webp':
            emote = open('emotes/'+file, 'rb')
            res = bot.send_sticker(message.chat.id, emote)
            print(res)
        time.sleep(1)

if __name__ == '__main__':
    bot.polling(none_stop=False)
