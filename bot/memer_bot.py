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
                     data='CAADAgADnAADAm8gSUlfehpJdSSnAg')

@bot.message_handler(commands=['Kappa128', 'kappa128'])
def provide_kappa128(message):
    bot.send_sticker(chat_id=message.chat.id,
                     data='CAADAgADmwADAm8gSeu5xOY0kZaQAg')

@bot.message_handler(commands=['Kappa256', 'kappa256'])
def provide_kappa256(message):
    bot.send_sticker(chat_id=message.chat.id,
                     data='CAADAgADmgADAm8gSVEl3iquPsLtAg')


@bot.inline_handler(lambda query: len(query.query) is 0)
def empty_query(query):
    hint = 'Afloat query to support memes movement! Type Kappa until it is too late!'
    try:
        q = types.InlineQueryResultArticle(
            id='0', title='Meme Master',
            description=hint,
            input_message_content=types.InputTextMessageContent(
                message_text="I'd like you to type Kappa, please. That's what this query is solely about."
            )
        )
        bot.answer_inline_query(query.id, [q], cache_time=3600)

    except Exception as e:
        print(e)

@bot.inline_handler(lambda query: str(query.query) == 'Kappa')
def provide_query_kappa(query):
    try:
        kappa_128 = types.InlineQueryResultCachedSticker(id='1', sticker_file_id='CAADAgADmwADAm8gSeu5xOY0kZaQAg')
        kappa_192 = types.InlineQueryResultCachedSticker(id='2', sticker_file_id='CAADAgADnAADAm8gSUlfehpJdSSnAg')
        kappa_256 = types.InlineQueryResultCachedSticker(id='3', sticker_file_id='CAADAgADmgADAm8gSVEl3iquPsLtAg')
        bot.answer_inline_query(query.id, [kappa_128, kappa_192, kappa_256], cache_time=3600)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    random.seed()
    bot.polling(none_stop=True)
