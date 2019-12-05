import random
import telebot
import http.client
import requests
from telebot.types import Message

TOKEN = '1050352227:AAFOlAIgyONQ7S57QwP9qSszixetcX80b7M'
bot = telebot.TeleBot(TOKEN)

stickers = ["CAADAgADCgADxFelFw1tU6rKV8MdFgQ",
            "CAADAgADCwADxFelF8LdHaU-IgR8FgQ",
            "CAADAgADDAADxFelF9YUb-GVqFXsFgQ",
            "CAADAgADDQADxFelF-YygTYkoBeFFgQ",
            "CAADAgADDgADxFelF_61MNW1f_PcFgQ",
            "CAADAgADDwADxFelF0HwSN86xJ4QFgQ",
            "CAADAgADEAADxFelF-5ip6XJ3MpGFgQ",
            "CAADAgADEQADxFelF_qpWhd-UkDJFgQ",
            "CAADAgADEgADxFelF5kOKCLO9A6zFgQ",
            "CAADAgADEwADxFelF1eUe1aXiwgwFgQ",
            "CAADAgADFAADxFelF7AfUw0FsXwsFgQ",
            "CAADAgADFQADxFelF7ye60hhiwH7FgQ",
            "CAADAgADFgADxFelF9Hg_Ot-XbXbFgQ",
            "CAADAgADFwADxFelFyX3sdAC9V6EFgQ",
            "CAADAgADGAADxFelF2fuXwKYzANOFgQ",
            "CAADAgADGQADxFelF-LTqB6HsQz_FgQ"]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Вас приветствует бот, знающий все о погоде. Введите название города на английском языке, чтобы получить информацию о погоде в нем.")

@bot.message_handler(func = lambda message: True)
def weather(message: Message):
    url = "https://devru-latitude-longitude-find-v1.p.rapidapi.com/latlon.php"

    querystring = {"location": f"{message.text}"}

    headers = {
        'x-rapidapi-host': "devru-latitude-longitude-find-v1.p.rapidapi.com",
        'x-rapidapi-key': "f041a47b13mshe0b82bfe02f2225p167efajsnd18148491ad8"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    lat = ""
    lon = ""
    try:
        lat = response.json()['Results'][0]['lat']
        lon = response.json()['Results'][0]['lon']
    except:
        bot.reply_to(message,
                     "Некорректное название города. Попробуйте еще раз.")
        return True

    url = f"https://api.darksky.net/forecast/f85cb37ea3ecc6b8c61a052f04006013/{lat},{lon}"

    querystring = {"lang": "en", "lon": f"{lon}", "lat": f"{lat}"}

    headers = {
        'x-rapidapi-host': "dark-sky.p.rapidapi.com",
        'x-rapidapi-key': "f041a47b13mshe0b82bfe02f2225p167efajsnd18148491ad8"
    }

    response = requests.get(url)
    temp = response.json()['currently']['temperature']
    dtemp = float(temp)
    newtemp = (dtemp - 32)*5/9
    newesttemp = round(newtemp, 2)
    visibility = response.json()['currently']['visibility']
    dvis = float(visibility)
    newvisibility = dvis*1.609
    newestvisibility = round(newvisibility, 3) * 1000
    windSpeed = response.json()['currently']['windSpeed']
    dwind = float(windSpeed)
    newwind = dwind/2.237
    newestwind = round(newwind,2)
    city = f"{message.text}"
    bot.reply_to(message, f"Информация по городу {city} \n Температура воздухa: {newesttemp} °C \n  Видимость: {newestvisibility} метров\n Скорость ветра: {newestwind} м/с")

bot.polling()