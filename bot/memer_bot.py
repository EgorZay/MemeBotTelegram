# -*- coding: utf-8 -*-

import telebot
from telebot import types
import random
import time
import config
import re
import requests

class Preprocessor(object):

    @staticmethod
    def randomize_postbase(soft=True):
            if soft == True:
                return random.randint(1, 9)
            else:
                return random.randint(100, 999)

    @staticmethod
    def prepare_url():
        url = url_dict['prebase'] + url_dict['base']
        additive = '13' + str(Preprocessor.randomize_postbase(soft=True)) + '0' + str(Preprocessor.randomize_postbase(soft=False))
        return url, additive

    @staticmethod
    def get_title():
        content = requests.get(url_dict['base_title'] + Preprocessor.prepare_url()[1])
        caption = re.search('og:title" content="(.+?)"', content.text)
        return caption.group(1)

url_dict = {
    'base_title': config.base_title,
    'prebase': config.prebase,
    'base': config.base}

bot = telebot.TeleBot(token=config.token)
@bot.message_handler(commands=['meme', 'Meme'])
def provide_meme(message):
    bot.send_photo(chat_id=message.chat.id,
                   photo=''.join(Preprocessor.prepare_url()[i] for i in range(2)),
                   caption=Preprocessor.get_title())
    time.sleep(1)

@bot.message_handler(commands=['Kappa', 'kappa'])
def provide_kappa(message):
    bot.send_sticker(chat_id=message.chat.id,
                     data='CAADAgADiAADqY0YSffyaTQRASc3Ag')

@bot.message_handler(commands=['Kappa128', 'kappa128'])
def provide_kappa128(message):
    bot.send_sticker(chat_id=message.chat.id,
                     data='CAADAgADhwADqY0YSfvhSoAVRdGjAg')

@bot.message_handler(commands=['Kappa256', 'kappa256'])
def provide_kappa256(message):
    bot.send_sticker(chat_id=message.chat.id,
                     data='CAADAgADhgADqY0YSWMq0_yxYGUtAg')

#TODO: implement inline_handler

if __name__ == '__main__':
    random.seed()
    bot.polling(none_stop=True)
