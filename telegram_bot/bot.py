import hashlib

from youtube_search import YoutubeSearch
from aiogram import Bot, types, utils
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from aiogram.utils import executor
from aiogram.utils.markdown import link
from config import open_weather_token
from asyncio import sleep

import markups as nav
import requests
import datetime
import os
import json
import string
import logging
import hashlib

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(text='/start')
async def echo_send(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}!\n'
                         f'Ваш id: {message.from_user.id}', reply_markup=nav.mainMenu)


@dp.message_handler(text='Python')
async def echo_send(message: types.Message):
    await bot.send_message(message.from_user.id, 'Держите', reply_markup=nav.mainIn)


@dp.message_handler(text='Другое')
async def echo_send(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в раздел "Другое"', reply_markup=nav.otherMenu)


@dp.message_handler(text='Аватар')
async def echo_send(message: types.Message):
    photo = open('Vacunto.png', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.message_handler(text='Справочник')
async def echo_send(message: types.Message):
    await message.answer(f'Тут подробно описанно ка пользоватся ботом!\n'
                         f'Если вы хотите узнать погоду, нажмите на кнопку "Погода" и следуйте инструкции\n'
                         f'Если вы хотите найти и скинуть видео с ютуба челевеку или на канал - пропишите @vacuntosbot (название ролика)\n'
                         f'Для изучения питона нажмите кнопку "Python" и следуйте инструкции\n'
                         f'Если вы хотите с играть в кости с ботом нажмите кнопку "Игра"\n'
                         f'Маты запрещены!',
                         reply_markup=nav.otherMenu)


@dp.message_handler(text='Игра')
async def echo_send(message: types.Message):
    await bot.send_message(message.from_user.id, 'Игра начинается', reply_markup=nav.otherMenu)
    await sleep(1)

    bot_data = await bot.send_dice(message.from_user.id)
    bot_data = bot_data['dice']['value']
    await sleep(5)

    user_data = await bot.send_dice(message.from_user.id)
    user_data = user_data['dice']['value']
    await sleep(5)

    if bot_data > user_data:
        await bot.send_message(message.from_user.id, 'Вы проиграли')
    elif bot_data < user_data:
        await bot.send_message(message.from_user.id, 'Вы победили')
    else:
        await bot.send_message(message.from_user.id, 'Ничья')


@dp.message_handler(text='Главное меню')
async def echo_send(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в раздел "Главное меню"', reply_markup=nav.mainMenu)

def searcher(text):
    res = YoutubeSearch(text, max_results=10).to_dict()
    return res


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}'
        )
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)


@dp.message_handler(text='Погода')
async def echo_send(message: types.Message):
    await message.reply('Напиши мне название города')


@dp.message_handler()
async def echo_send(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно  \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')

        data = r.json()

        city = data['name']
        coord_lat = data['coord']['lat']
        coord_lon = data['coord']['lon']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Не понятно что там, посмотри в окно)"

        cur_humidity = data['main']['humidity']
        cur_country = data['sys']['country']
        cur_speed = data['wind']['speed']

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f'Страна: {cur_country}\nКоординаты: {coord_lat} {coord_lon}\nПогода в городе: {city}\n'
                            f'Температура: {cur_weather}C {wd}\nВлажность: {cur_humidity}%\nВетер: {cur_speed}\n'
                            f'Хорошего вам дня!')

    except:
        pass
        # await message.reply('\U00002620 Не понимаю Вас \U00002620')


@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().traslate(str.maketrans('', '', string.punctuation)) for i in message.text.split('')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
