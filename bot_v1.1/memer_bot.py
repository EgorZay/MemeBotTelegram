import requests
import time
import telebot
import random
import config

import numpy as np
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

num = 0
link_list = 0
length = 0
array = 0
base = 'https://imgur.com'


def global_refresh(url=base, agent=UserAgent().chrome):
    response = requests.get(url=url, headers={
        'User-Agent': agent})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find(None, attrs={'class': 'cards'})
    tags = cards.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['image-list-link'])
    link_list_ = [link.attrs['href'] for link in tags]

    return link_list_, link_list_.__len__()


def randomize():
    global link_list
    global length
    global num
    global array

    array = np.arange(0, length)
    num = random.choice(array)
    array = np.delete(array, array[num])
    length -= 1

    return num


def get_meme(url=base, agent=UserAgent().chrome):
    response = requests.get(url + link_list[randomize()], headers={
        'User-Agent': agent})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find(None, attrs={'class': 'left post-pad'})
    src = card.find(None, attrs={'class': 'post-images'})
    meme = src.find(itemprop='contentURL').get('content')
    if meme is None:
        meme = 'https:' + src.find(itemprop='contentURL').get('src')

    header = card.find(None, attrs={'class': 'post-header'})
    title = header.find('h1', attrs={'class': 'post-title'}).text

    return meme, title


bot = telebot.TeleBot(token=config.token)


@bot.message_handler(commands=['refresh', 'Refresh'])
def bot_refresh(message):
    global link_list
    global length

    bot.send_message(chat_id=message.chat.id, text='Loading ...')
    bot.send_chat_action(chat_id=message.chat.id, action='typing')
    link_list, length = global_refresh()
    time.sleep(1)

    bot.send_message(chat_id=message.chat.id,
                     text=str('{} memes are loaded.').format(length))
    time.sleep(1)


@bot.message_handler(commands=['queue', 'Queue'])
def bot_queue(message):
    bot.send_message(chat_id=message.chat.id,
                     text=str('{} memes left'.format(length)))
    time.sleep(1)


@bot.message_handler(commands=['meme', 'Meme'])
def bot_meme(message):
    if length < 1:
        bot.send_message(chat_id=message.chat.id,
                         text="Meme list is empty.\nTry '/refresh' prompt first.")
        time.sleep(1)

    meme, title = get_meme()
    if meme[-3:] in ['jpg', 'peg', 'png']:
        bot.send_photo(chat_id=message.chat.id,
                       photo=meme,
                       caption=title)
    elif meme[-3:] in ['mp4', 'gif']:
        bot.send_video(chat_id=message.chat.id,
                       data=meme,
                       caption=title)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Undefined format.\nRetry.')
    time.sleep(1)


if __name__ == '__main__':
    bot.polling(none_stop=True)
