from ctypes import string_at
from math import e
import webbrowser
import psutil
import speech_recognition as sr
import pyttsx3
from sound import Sound
import urllib
import geocoder
import pymorphy2
import smtplib
import playsound
from pytube import YouTube
import time
import pytesseract
from PIL import Image
import pycountry
from time import sleep
from colorama import init, Fore
import time
from suntime import Sun, SunTimeException
import cv2
import ast
import urllib
from urllib import request
import random
import arrow
import psutil
import screen_brightness_control as sbc
import pyautogui, time
from time import sleep
import string
import sys
from translate import Translator
from datetime import date, timedelta
from win10toast import ToastNotifier
import time
import requests
import wave
import re
import re
import json
from urllib.request import urlopen
import datetime
import pyperclip
import subprocess
import os
from pycbrf.toolbox import ExchangeRates
import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import smtplib # Модуль для работы с почтой
import wikipedia as wiki
import re
import codecs
from tqdm import tqdm, tqdm_gui, trange
import pickledb
import sys
import os.path
import bs4, requests
import re
import smtplib
import datetime
import telebot
import getpass
import platform as pf
import rich
# -*- coding: utf-8 -*-
toast = ToastNotifier()
#Проверка файлов
proverkafile = os.path.exists('envelope.py') # False
proverkafile2 = os.path.exists('sound.py') # False
proverkafile3 = os.path.exists('keyboard.py') # False
proverkafile4 = os.path.exists('haarcascade_frontalface_default.xml')
proverkafile5 = os.path.exists('photos') # False, папка существует но это не файл.
proverkafile = str(proverkafile)
proverkafile2 = str(proverkafile2)
proverkafile3 = str(proverkafile3)
proverkafile4 = str(proverkafile4)
proverkafile5 = str(proverkafile5)
print(proverkafile5)
if proverkafile5 == "False":
    print("Создайте папку с именем photos, для запуска Вторника")
    exit()
elif proverkafile == "False":
    print("У вас нету дополнительных файлов, скачайте архив по сыллке - https://drive.google.com/file/d/1n_t_r87I25YA_GeqKFYZyY3okIZrTOji/view?usp=sharing ")
    exit()
elif proverkafile2 == "False":
    print("У вас нету дополнительных файлов, скачайте архив по сыллке - https://drive.google.com/file/d/1n_t_r87I25YA_GeqKFYZyY3okIZrTOji/view?usp=sharing ")
    exit()
elif proverkafile3 == "False":
    print("У вас нету дополнительных файлов, скачайте архив по сыллке - https://drive.google.com/file/d/1n_t_r87I25YA_GeqKFYZyY3okIZrTOji/view?usp=sharing ")
    exit()
elif proverkafile4 == "False":
    print("У вас нету дополнительных файлов, скачайте архив по сыллке - https://drive.google.com/file/d/1n_t_r87I25YA_GeqKFYZyY3okIZrTOji/view?usp=sharing ")
    exit()

print("Файлы проверенны - успешно")

dbnew = pickledb.load("api.db", True)
if not dbnew.exists("api"):
    dbnew.set("login", "Vtornik")
    dbnew.set("api", input("Апи ключ для https://audd.io "))
else:
    print("\nДобрый день, {}!".format(dbnew.get("login")),
    "\n Вы успешно авторизованы!")

items = list(range(0, 50))
l = len(items)


opts = {
    "alias": ("Вторник", "вторник", "вторничок")

}

wiki.set_lang('ru')

#инициализируем модули
r = sr.Recognizer()
mic = sr.Microphone()
tts = pyttsx3.init('sapi5')
voices = tts.getProperty('voices')
tts.setProperty('voice', 'ru') 

with mic as source:
	r.adjust_for_ambient_noise(source)

def get_internet_connection():
	try:
		urllib.request.urlopen('http://yandex.ru')
		return True
	except IOError:
		return False

for voice in voices:
    if voice.name == 'Irina':
        tts.setProperty('voice', voice.id)

def say(text):
	tts.say(text)
	tts.runAndWait()

def recognize():
	try:
		with mic as source:
			audio = r.listen(source)
			text = r.recognize_google(audio, language = 'ru_RU')
			return text.lower()
	except sr.UnknownValueError:
		return recognize()
	except sr.RequestError:
		say('У меня нет доступа к серверам Гугл для распознавания вашей речи!')

def get_sentence_without_elems(sent):
	return re.sub(r'\(.*?\)', '', sent)

def what_is_it(sent):
	try:
		w = sent.split()
		d = ["кто"]
		for i in w:
			if i not in []:
				d.append(i)
		s2 = ' '.join(d)
		result = get_sentence_without_elems(wiki.summary(s2, sentences = 2))
		say(result)
	except wiki.exceptions.PageError:
		say('Извините, я не знаю этого')
	except:
		say('Извините, но в модуле Википедии произошла неизвестная ошибка!!!')

is_internet = get_internet_connection()
last_check_time = time.time()
period_checking = 120

init(autoreset=True)

try:
    urllib.request.urlopen('http://google.com')
    print("\033[32m" + "WI-FI connection true")
    time.sleep(5)
except:
    print("\033[31m" + "WI-FI connection false")
    exit()

def loadbar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='>'):
	percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} {percent}', end='\r')
	if iteration == total:
		print()

items = list(range(0, 50))
l = len(items)

loadbar(0, l, prefix='\033[32m' + 'loading..', suffix='Complete', length=l)
for i, item in enumerate(items):
	sleep(0.1)
	loadbar(i + 1, l, prefix='\033[32m' + 'loading..', suffix='Complete', length=l)
time.sleep(4)
def show_notify(title, text):
    toast.show_toast(title, text, duration=5, icon_path="icon.ico")

print('\033[32m' + 'succefull')


nowvremya = datetime.datetime.now().strftime('%H')
print(nowvremya)
nownowvremya = str(nowvremya)
print(nownowvremya)
if int(nownowvremya) >= 0 and int(nownowvremya) <= 5:
	say("Доброй ночи")
elif int(nownowvremya) >= 6 and int(nownowvremya) <= 11:
	say("Доброе утро")
elif int(nownowvremya) >= 12 and int(nownowvremya) <= 17:
	say("Добрый день")
elif int(nownowvremya) >= 18 and int(nownowvremya) <= 24:
	say("Добрый вечер")
else:
	print('Неизвестное время')

db = pickledb.load("information.db", True)
proverka = db.get("tommorow")
proverka2 = db.get("napomination")
date_Today = datetime.datetime.today().strftime("%Y-%m-%d")
if proverka == date_Today:
	show_notify("Напоминание Вторник", proverka2)
	db.rem("tommorow")
	db.rem("napomination")
else:
	print("Загружаю систему..")

while True:
	if (time.time() - last_check_time) > period_checking:
		with mic as source:
			r.adjust_for_ambient_noise(source)
		is_internet = get_internet_connection()
		last_check_time = time.time()

	if (is_internet):
		cmd = recognize()
		for x in opts['alias']:
			cmd = cmd.replace(x, "").strip()
			print("[log] Распознано: " + cmd)
		if  "ответь на вопрос" in cmd:
			a = cmd.replace("ответь на вопрос ", "")
			url = "https://otvet.mail.ru/go-proxy/answer_json?q=" + a
			print(url)
			response = requests.get(url)
			bs = BeautifulSoup(response.text, "lxml")
			soup = BeautifulSoup(response.content, 'html.parser')
			data2 = soup.find('body')
			soup = str(soup)
			soup = soup.split('url"', 1)[1].lstrip()
			soup = soup[ 0 : soup.index(',')]
			soup = soup.replace('"', "")
			soup = soup[1:]
			print(soup)
			webbrowser.open(soup)
		elif "погода" in cmd:
			url = 'https://nova.rambler.ru/search?query=погода'
			response = requests.get(url)
			bs = BeautifulSoup(response.text, "lxml")
			soup = BeautifulSoup(response.content, 'html.parser')
			data = soup.find('body')
			km = data.find('div', class_="MixinWeather__temperature--2S3F4")
			km2 = km.find_next('div', class_="MixinWeather__temperature--2S3F4")
			km3 = km2.find_next('div', class_="MixinWeather__temperature--2S3F4")
			km4 = km3.find_next('div', class_="MixinWeather__temperature--2S3F4")
			km5 = km4.find_next('div', class_="MixinWeather__temperature--2S3F4")
			km6 = km5.find_next('div', class_="MixinWeather__temperature--2S3F4")
			km2 = km2.text
			km2 = str(km2).replace("°", "° ")
			km3 = km3.text
			km3 = str(km3).replace("°", "° ")
			km4 = km4.text
			km4 = str(km4).replace("°", "° ")
			km5 = km5.text
			km5 = str(km5).replace("°", "° ")
			km6 = km6.text
			km6 = str(km6).replace("°", "° ")
			time = data.find('div', class_="MixinWeather__weekday--cs99M")
			time2 = time.find_next('div', class_="MixinWeather__weekday--cs99M")
			time3 = time2.find_next('div', class_="MixinWeather__weekday--cs99M")
			time4 = time3.find_next('div', class_="MixinWeather__weekday--cs99M")
			time5 = time4.find_next('div', class_="MixinWeather__weekday--cs99M")
			time6 = time5.find_next('div', class_="MixinWeather__weekday--cs99M")
			km = km.text
			km = str(km).replace("°", "° ")
			say(km + " - погода на " + time.text + "\n" + km2 + " - погода на " + time2.text + "\n" + km3 + " - погода на " + time3.text + "\n" + km4 + " - погода на " + time4.text + "\n" + km5 + " - погода на " + time5.text + "\n" + km6 + " - погода на " + time6.text + "\n")
			print(km + " - погода на " + time.text + "\n" + km2 + " - погода на " + time2.text + "\n" + km3 + " - погода на " + time3.text + "\n" + km4 + " - погода на " + time4.text + "\n" + km5 + " - погода на " + time5.text + "\n" + km6 + " - погода на " + time6.text + "\n")
		elif "во сколько сегодня сядет солнце" in cmd or "во сколько сегодня закат" in cmd:
			g = geocoder.ip('me')
			gg = g.latlng
			rep = re.compile('s/^0-9.*//g')
			print (gg)
			ggggglat = str(gg).split(',', 1)[1].lstrip()
			ggggglat1 = ggggglat[:-1]
			print(ggggglat1)
			ggggglong = str(gg).split(",")[0]
			ggggglong1 = ggggglong[1:]
			print(ggggglong1)
			print(ggggglat1)
			latitude = float(ggggglat1)
			longitude = float(ggggglong1)
			sun = Sun(latitude, longitude)
			yeara = int(datetime.datetime.today().strftime('%Y'))
			monta = int(datetime.datetime.today().strftime('%m'))
			daya = int(datetime.datetime.today().strftime('%d'))
			abd = datetime.date(yeara, monta, daya)
			abd_sr = sun.get_local_sunrise_time(abd)
			abd_ss = sun.get_local_sunset_time(abd)
			say('В {} солнце встает в {} и сядет в {}.'.
      			format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))
			print('В {} солнце встает в {} и сядет в {}.'.
      			format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))
			url = 'http://ipinfo.io/json'
			response = urlopen(url)
			data = json.load(response)

			IP=data['ip']
			org=data['org']
			city = data['city']
			country=data['country']
			region=data['region']
			say("В городе" + " " + city + " " + "в стране" + " " + country)
			print(city, country)
			print("В городе" + " " + city + " " + "в стране" + " " + country)

		elif "во сколько сегодня рассвет солнца" in cmd or "во сколько сегодня рассвет" in cmd:
			g = geocoder.ip('me')
			gg = g.latlng
			rep = re.compile('s/^0-9.*//g')
			print (gg)
			ggggglat = str(gg).split(',', 1)[1].lstrip()
			ggggglat1 = ggggglat[:-1]
			print(ggggglat1)
			ggggglong = str(gg).split(",")[0]
			ggggglong1 = ggggglong[1:]
			print(ggggglong1)
			print(ggggglat1)
			latitude = float(ggggglat1)
			longitude = float(ggggglong1)
			sun = Sun(latitude, longitude)
			yeara = int(datetime.datetime.today().strftime('%Y'))
			monta = int(datetime.datetime.today().strftime('%m'))
			daya = int(datetime.datetime.today().strftime('%d'))
			abd = datetime.date(yeara, monta, daya)
			abd_sr = sun.get_local_sunrise_time(abd)
			abd_ss = sun.get_local_sunset_time(abd)
			say('В {} солнце встает в {} и сядет в {}.'.
      			format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))
			print('В {} солнце встает в {} и сядет в {}.'.
      			format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))
			url = 'http://ipinfo.io/json'
			response = urlopen(url)
			data = json.load(response)

			IP=data['ip']
			org=data['org']
			city = data['city']
			country=data['country']
			region=data['region']
			say("В городе" + " " + city + " " + "в стране" + " " + country)
			print(city, country)
			print("В городе" + " " + city + " " + "в стране" + " " + country)
		#из картинки в текст
		elif "в текст" in cmd:
			say("Смотрите командную строку")
			strana = input("Напишите страну на английском языке:")

			if strana == "Russia":
				strana = "Russian Federation"

			elif strana == "russia":
				strana = "Russian Federation"
			latin = pycountry.countries.lookup(strana)

			print(latin.alpha_3)

			put = input("Укажите название файла: ")

			img = Image.open(put)

			pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

			custom_config = r'--oem 3 --psm 13'
			text = pytesseract.image_to_string(img, lang=latin.alpha_3)
			print(text.strip())
		#пробки
		elif "пробки" in cmd or "покажи пробки" in cmd or "пробки в" in cmd:
			say("Открываю сайт с пробками, смотрите внимательно!")
			webbrowser.open ("https://yandex.kz/maps/?l=trf%2Ctrfe&ll=51.144188%2C43.656261&z=14")
		
		#установка "видео с ютуба"
		elif "скачай видео" in cmd or "установи видео" in cmd:
			say("Вставьте сыллку на видео в командную строку")
			url = input("Вставьте сыллку ")
			print("Процесс")
			yt = YouTube(url)
			title = yt.title
			streams = yt.streams.get_by_itag(22)
			print('\033[32m' + "downloading (    {}    ), please wait ...".format(title))
			streams.download()
			print('\033[32m' + 'done')

				
		#браузер
		elif "домой" in cmd:
			webbrowser.open ("https://google.ru", new=2)
		elif "открыть новое окно инкогнито" in cmd or "новое окно инкогнито" in cmd or "инкогнито" in cmd or "перейди в режим инкогнито" in cmd:
			pyautogui.hotkey("ctrl", "shift", "n")
		elif "предыдущая страница" in cmd or "на страницу назад" in cmd:
			pyautogui.hotkey("alt", "left")
		
		elif "добавь эту страницу в закладки" in cmd:
			pyautogui.hotkey("ctrl", "d")

		elif "обнови страницу" in cmd:
			pyautogui.hotkey("ctrl", "r")

		elif "очистка истории" in cmd or "очисти историю" in cmd or "очистить историю" in cmd or "очисти историю браузера" in cmd:
			webbrowser.open ("opera://settings/clearBrowserData")
		
		elif "открыть консоль" in cmd:
			pyautogui.hotkey("ctrl", "shift", "j")
		elif "открыть инструменты" in cmd:
			pyautogui.hotkey("ctrl", "shift", "i")
		elif "исходный код страницы" in cmd or "открыть исходный код страницы" in cmd or "показать исходный код страницы" in cmd:
			pyautogui.hotkey("ctrl", "u")
		elif "показать окно закладок" in cmd:
			pyautogui.hotkey("ctrl", "shift", "b")
		elif "перейти в загрузки" in cmd:
			pyautogui.hotkey("ctrl", "j")
		elif "перейти в историю" in cmd:
			pyautogui.hotkey("ctrl", "h")
		
		#навигация по странице

		elif "увеличить страницу" in cmd:
			pyautogui.hotkey("ctrl", "+")
		
		elif "уменьшить страницу" in cmd:
			pyautogui.hotkey("ctrl", "-")
		elif "поиск" in cmd:
			pyautogui.hotkey("ctrl", "f")
		elif "выше" in cmd:
			pyautogui.hotkey("shift", "space")
		elif "ниже" in cmd:
			pyautogui.press("space")
		elif "вверх" in cmd:
			pyautogui.press("home")
		elif "вниз" in cmd:
			pyautogui.press("end")

		

		#навигация по вкладкам

		elif "следующая вкладка" in cmd:
			pyautogui.hotkey("ctrl", "tab")
		elif "предыдущая вкладка" in cmd:
			pyautogui.hotkey("ctrl", "shift", "tab")
		
		#google keep
		elif "закончить редактирование" in cmd:
			pyautogui.press("esc")

		elif "изменить вид" in cmd:
			pyautogui.hotkey("ctrl", "shift", "d", "8")

		elif "архивировать заметку" in cmd:
			pyautogui.press("e")
		elif "отправить в корзину заметку" in cmd:
			pyautogui.hotkey("delete")
		elif "закрепить заметку" in cmd:
			pyautogui.press("f")
		elif "google keep" in cmd or "гугл кип" in cmd or "заметки гугл" in cmd or "заметки" in cmd:
			webbrowser.open("https://keep.google.com/u/0/#home")
			pyautogui.press("tab")
		elif "создать заметку" in cmd:
			pyautogui.press("c")
		elif "создать список" in cmd:
			pyautogui.press("l")
		elif "выбрать всё заметки" in cmd:
			pyautogui.hotkey("ctrl", "a")
		elif "перейти к следующей заметке" in cmd:
			pyautogui.press("j")
		elif "перейти к предыдущей заметке" in cmd:
			pyautogui.press("k")
		elif "переместить заметку вперёд" in cmd:
			pyautogui.hotkey("shift", "k")
		elif "переместить заметку назад" in cmd:
			pyautogui.hotkey("shift", "j")
		elif "перейти к следующему пункту" in cmd:
			pyautogui.press("n")
		elif "перейти к предыдущему пункту" in cmd:
			pyautogui.press("p")
		elif "переместить пункт вверх" in cmd:
		    pyautogui.hotkey("shift", "p")
		elif "переместить пункт вниз" in cmd:
		    pyautogui.hotkey("shift", "n")
		elif "заметки" in cmd:
 		   webbrowser.open("https://keep.google.com/#home")
		elif "напоминания" in cmd:
			webbrowser.open("https://keep.google.com/#reminders")
		elif "архив" in cmd:
			webbrowser.open("https://keep.google.com/#archive")
		elif "корзина" in cmd:
			webbrowser.open("https://keep.google.com/#trash")

		#винда команды

		elif "вырезать" in cmd:
			pyautogui.hotkey("ctrl", "x")
		elif "копировать" in cmd or "скопировать" in cmd:
			pyautogui.hotkey("ctrl", "c")
		elif "копировать всё" in cmd or "скопировать всё" in cmd:
			pyautogui.hotkey("ctrl", "a")
			pyautogui.hotkey("ctrl", "c")
		elif "отменить" in cmd or "отменить действие" in cmd or "отменить последнее действие" in cmd:
			pyautogui.hotkey("ctrl", "z")
		elif "отменить перевод" in cmd:
			pyautogui.hotkey("ctrl", "shift", "z")
		elif "новый файл" in cmd:
			pyautogui.hotkey("ctrl", "n")
		elif "закрыть окно" in cmd:
			pyautogui.hotkey("ctrl", "w")
		elif "печать" in cmd:
			pyautogui.hotkey("ctrl", "p")
		elif "открыть поиск виндовс" in cmd or "открыть поиск windows" in cmd:
			pyautogui.hotkey("win", "s")
		elif "вставить" in cmd:
			pyautogui.hotkey("ctrl", "v")
		elif "скрыть все окна" in cmd:
			pyautogui.hotkey("win", "m")
		elif "открыть пуск" in cmd:
			pyautogui.hotkey("ctrl", "esc")
		elif "открыть запуск" in cmd:
			pyautogui.hotkey("win", "r")
		elif "мой компьютер" in cmd:
			pyautogui.hotkey("win", "e")
		elif "на весь экран" in cmd:
			pyautogui.hotkey("alt", "enter")
		elif "открыть контекстное меню" in cmd:
			pyautogui.hotkey("shift", "f10")

		elif "выйти из системы" in cmd or "заверши сеанс" in cmd:
			pyautogui.hotkey("win", "l")
		elif "закрыть программу" in cmd or "завершить программу" in cmd or "убить программу" in cmd or "закрыть игру" in cmd or "выйти из игры" in cmd:
			pyautogui.hotkey("alt", "f4")
		elif "создать новую папку" in cmd or "новая папка" in cmd:
			pyautogui.hotkey("ctrl", "shift", "n")
		elif "открыть диспетчер задач" in cmd:
			pyautogui.hotkey("ctrl", "shift", "esc")
		elif "открыть все окна" in cmd:
			pyautogui.hotkey("win", "shift", "m")
		elif "окна в право" in cmd or "программа вправо" in cmd or "перевести всё в право" in cmd or "программа в правом" in cmd:
			pyautogui.hotkey("winleft", "right")
		elif "свернуть программу" in cmd or "свернуть" in cmd or "свернуть окно" in cmd:
			pyautogui.hotkey("winleft", "down")
		elif "развернуть" in cmd or "на весь экран" in cmd or "во весь экран" in cmd or "сделать на весь экран" in cmd:
			pyautogui.hotkey("winleft", "up")
		elif "всё в лево" in cmd or "окно влево" in cmd or "программа в лево" in cmd or "программа в левом" in cmd:
			pyautogui.hotkey("winleft", "left")
		elif "следующее окно" in cmd or "другое окно" in cmd or "следующая программа" in cmd or "другая программа" in cmd:
			pyautogui.hotkey("alt", "esc")
		elif "таблица символов" in cmd or "смайлики" in cmd or "эмодзи" in cmd or "юникод" in cmd:
			pyautogui.hotkey("win", ";")
		elif "сменить окно" in cmd:
			pyautogui.keyDown('alt')
			time.sleep(0.100)
			pyautogui.press("tab")
			pyautogui.keyUp("alt")
		#shazam
		elif "узнай песню" in cmd:
			print("В разработке")
		elif "перейди на" in cmd:
			okno = new_str = cmd.replace("перейди на", "")
			oknop = okno = okno.replace(" ", "")
			obeb = oknop = oknop.replace("окно", "")
			obeb2 = obeb = obeb.replace("окон", "")
			oknoint = int(obeb2)
			pyautogui.keyDown('alt')
			time.sleep(0.100)
			pyautogui.press("tab")
			for i in range(oknoint):
				pyautogui.press("tab")
			pyautogui.rightClick()
			pyautogui.keyUp("alt")
			
		elif 'открой' in cmd or 'запусти' in cmd or "перейди" in cmd:
			if 'браузер' in cmd or 'chrome' in cmd:
				say("В разработке")
			elif "диспетчер" in cmd:
				pyautogui.hotkey("shift", "esc")
			elif "в ютуби" in cmd:
				youtubeopen = new_str = cmd.replace("открой в ютуби", "")
				youtubeopen1 = youtubeopen = youtubeopen.replace(" ", "")
				webbrowser.open ("https://www.youtube.com/results?search_query=" + youtubeopen1)
				say("Открыл")
			elif "вкладку" in cmd:
				pyautogui.hotkey("ctrl", "t")
			elif 'unity' in cmd or 'юнити' in cmd:
				say("Запрос выполнен сэр")
				subprocess.Popen('C:/Program Files/Unity/Editor/Unity.exe')
			elif "steam" in cmd or "стим" in cmd:
				say("Запрос выполнен сэр")
				subprocess.Popen('C:/Program Files (x86)/Steam/steam.exe')

			elif "курс валют" in cmd or "курс валют" in cmd:
				say("Запрос выполнен сэр")
				webbrowser.open ('https://profin.kz/converter/', new=2)

			elif "ютуб" in cmd or "youtube" in cmd or "в youtube" in cmd or "в ютуб" in cmd:
				say("Запрос выполнен сэр")
				webbrowser.open ("https://www.youtube.com", new=2)

			elif "vk" in cmd or "вк" in cmd or "в вк" in cmd:
				say("Запрос выполнен сэр")
				webbrowser.open ("https://vk.com", new=2)

			elif "закрытую вкладку" in cmd:
				pyautogui.hotkey("ctrl", "shift", "t")
			
			elif "google" in cmd or "гугл" in cmd or "в гугл" in cmd:
				say("Запрос выполнен сэр")
				webbrowser.open ("https://www.google.ru", new=2)

		elif 'закрой' in cmd:
			if 'браузер' in cmd or 'chrome' in cmd or 'google' in cmd:
				os.system('TASKKILL /F /IM opera.exe')
			elif "вкладку" in cmd:
				pyautogui.hotkey("ctrl", "f4")
			elif "закрытую вкладку" in cmd:
				pyautogui.hotkey("ctrl", "f4")
			elif 'unity' in cmd or 'юнити' in cmd:
				say("Хорошо")
				os.system('TASKKILL /F /IM Unity.exe')
			elif "steam" in cmd or "стим" in cmd:
				say("Хорошо")
				os.system('TASKKILL /F /IM steam.exe')
			elif "file" in cmd or "файл" in cmd:
				say("Хорошо")
				os.system('TASKKILL /F /IM notepad.exe')
			elif "discord" in cmd or "дискорд" in cmd:
				say("Хорошо")
				os.system('TASKKILL /F /IM discord.exe')
			elif "архив" in cmd:
				say("Хорошо")
				os.system('TASKKILL /F /IM winrar.exe')
		elif "включи" in cmd or "поставь" in cmd:
			if "следующею" in cmd or "следующую" in cmd or "следущую музыку" in cmd:
				pyautogui.hotkey("nexttrack")
			elif "предыдущую" in cmd or "предыдущую музыку" in cmd or "предыдущая" in cmd:
				pyautogui.hotkey("prevtrack")
			elif "видео" in cmd or "видос" in cmd:
				pyautogui.hotkey("playpause")
				say("Включил")
			elif "спящий режим" in cmd:
				say("Включаю")
				os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

			elif "радио" in cmd:
				say("Хорошо")
				os.startfile('record_superchart_-_rr_2021-09-25.mp3')
			
			else:
				newmusic = new_str = cmd.replace("включи", "")
				print(newmusic)
				translator1123 = Translator(from_lang="russian",to_lang="english")
				translation = translator1123.translate(newmusic)
				translation = translation.lower()
				print(translation)
#рок
				if "russian rock" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/rusrock")
				elif "rock'n'roll" in translation or "rock and roll" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/rnr")
				elif "progressive rock" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/prog")
				elif "post-rock" in translation or "post rock" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/postrock")
				elif "new wave" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/newwave")
				elif "folk rock" in translation or "folk rock" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/folkrock")
				elif "stoner rock" in translation or "stonerrock" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/stonerrock")
				elif "hardrock" in translation or "hard rock" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/hardrock")
				elif "rock" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/allrock")
#поп
				elif "russian pop" in translation or "rus pop" in translation or "russianpop" in translation or "ruspop" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/ruspop")
				elif "disco" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/disco")
				elif "k-pop" in translation or "kpop" in translation or "k pop" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/kpop")
				elif "j-pop" in translation or "jpop" in translation or "j pop" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/japanesepop")
				elif "pop" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/pop")
#инди
				elif "local indie" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/local-indie")
				elif "indie" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/indie")
#метал
				elif "metal" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/metal")
				elif "progressive metal" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/progmetal")
				elif "epic metal" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/epicmetal")
				elif "folk metal" in translation or "folkmetal" in translation or "folk-metal" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/folkmetal")
				elif "industrial" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/industrial")
				elif "extreme metal" in translation or "extrememetal" in translation or "extreme-metal" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/extrememetal")
				elif "numetal" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/numetal")
				elif "classic metal" in translation or "classicmetal" in translation or "classic-metal" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/classicmetal")
#альтернатива
				elif "alterntive" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/alternative")
				elif "posthardcore" in translation or "post hardcore" in translation or "post-hardcore" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/posthardcore")
				elif "harcode" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/hardcore")
#электроника
				elif "electronica" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/electronics")
				elif "dubstep" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/dubstep")
				elif "experimental" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/experimental")
#танц.музыка
				elif "dance" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/dance")
				elif "house" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/house")
				elif "techno" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/techno")
				elif "trance" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/trance")
				elif "drama-n-base" in translation or "drama n base" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/dnb")
				elif "rap" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/rap")
				elif "russian rap" in translation or "rusrap" in translation or "rus rap" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/rusrap")
				elif "foreign rap" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/foreignrap")
#r&b
				elif "R&B" in translation or "r and b" in translation or "rb" in translation or "rnb" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/rnb")
				elif "soul" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/soul")
				elif "funk" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/funk")
#jazz
				elif "traditional jazz" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/tradjazz")
				elif "modern jazz" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/conjazz")
				elif "jazz" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/jazz")
#blues
				elif "blues" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/blues")
#регги
				elif "regge" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/reggae")
				elif "reggeton" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/reggaeton")
				elif "dub" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/dub")
#ska
				elif "sovietskaya" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/soviet")
				elif "ska" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/ska")
#punk
				elif "punk" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/punk")
#музыка мира
				elif "world music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/folk")
				elif "russian music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/rusfolk")
				elif "tatar music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/tatar")
				elif "celtic music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/celtic")
				elif "balkan music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/balkan")
				elif "euro music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/eurofolk")
				elif "jewish music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/jewish")
				elif "eastern music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/eastern")
				elif "african music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/african")
				elif "latin music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/latin")
				elif "american music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/american")
				elif "romances" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/romances")
				elif "argentine tango" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/argentinetango")
				elif "armenian music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/armenian")
				elif "georgian music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/georgian")
				elif "azerbaijani music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/azerbaijani")
				elif "caucasian music" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/caucasian")
#эстрада
				elif "estrada" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/estrada")
				elif "russian estrada" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/rusestrada")
#шансон
				elif "сhanson" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/shanson")
				elif "coutry" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/country")
				elif "nature sounds" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/naturesounds")
				elif "bard" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/bard")
				elif "children" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/forchildren")
				elif "fairy tales" in translation or "fairy tale" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/fairytales")
				elif "soundtrack" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/soundtrack")
				elif "film" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/films")
				elif "tv" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/tvseries")
				elif "animated" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/animated")
				elif "videogame" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/videogame")
				elif "musical" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/musical")
				elif "relax" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/relax")
				elif "lounge" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/lounge")
				elif "new age" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/newage")
				elif "meditation" in translation:
    					webbrowser.open("https://radio.yandex.ru/genre/meditation")
				else:
					if "музыку" in newmusic:
						pyautogui.hotkey("playpause")
						say("Включил")
					else:
						webbrowser.open("https://music.yandex.ru/search?text=" + newmusic[1:])
		elif "выключи" in cmd:
			if "радио" in cmd:
				say("Хорошо")
				os.system('TASKKILL /F /IM Music.UI.exe')
			elif "интернет" in cmd:
				say("Вы серъезно хотите выключить интернет? Без интернета я не смогу функционировать")
				say("Напишите в командную строку да, если вы хотите отключить интернет")
				otvet = input()
				if otvet == "Да":
					os.system('ipconfig/release')
					exit()
				else:
					print("Хорошо")
			elif "музыку" in cmd:
				pyautogui.hotkey("playpause")
				say("Выключил")
			elif "видос" in cmd:
				pyautogui.hotkey("playpause")
				say("Выключил")
		elif "найди на карте" in cmd:
			naidi = new_str = cmd.replace("найди на карте", "")
			webbrowser.open ("https://www.google.com/maps/search/" + naidi)
		elif 'выключи компьютер' in cmd:
			say("Хорошо")
			os.system('shutdown -s')
		elif 'перезагрузи компьютер' in cmd:
			say("Хорошо")
			os.system('shutdown -r -t 0')
		elif 'кто' in cmd:
			what_is_it(cmd)
		elif "сохрани файл" in cmd or "сохрани file" in cmd:
			say("Хорошо")
			pyautogui.hotkey('ctrlleft', 's')
			say("Сделал")
		elif "напиши" in cmd:
			say("Хорошо")
			print(cmd)
			newpisatel = new_str = cmd.replace("напиши", "")
			print (newpisatel)
			time.sleep(5)
			pyperclip.copy(newpisatel)
			spam = pyperclip.paste()
			pyautogui.hotkey('ctrlleft', 'v')

		elif "поставь следущую" in cmd or "следущую" in cmd:
			pyautogui.hotkey("nexttrack")
		elif "поставь предыдущую" in cmd or "предыдущую" in cmd:
			pyautogui.hotkey("prevtrack")
		elif "сколько" in cmd:
			if "сейчас время" in cmd or "сейчас время" in cmd or "время" in cmd:
				now = datetime.datetime.now()
				say("Сейчас " + str(now.hour) + ":" + str(now.minute))


		elif "перейди" in cmd:
			if "в режим блокировки" in cmd:
				pyautogui.hotkey("win", "l")
		elif "пауза" in cmd:
			pyautogui.hotkey("playpause")
			say("Выключил")

		elif "загугли" in cmd:
			newcmd = new_str = cmd.replace('загугли', '')
			print(newcmd)
			print(cmd)
			webbrowser.open ("www.google.com/search?q=" + newcmd, new=2)
			say("Запрос выполнен сэр")

		elif "переведи" in cmd:
			if "на английский" in cmd:
				print(cmd)
				newperevod = new_str = cmd.replace("переведи на английский", "")
				translator = Translator(from_lang="russian",to_lang="english")
				translation = translator.translate(newperevod)
				say(translation)
				print (translation)
		
			elif "на казахский" in cmd:
				print(cmd)
				newperevod = new_str = cmd.replace("переведи на казахский", "")
				translator = Translator(from_lang="russian",to_lang="kazakh")
				translation = translator.translate(newperevod)
				say(translation)
				print (translation)
	
		elif "сотри всё" in cmd or "стери всё" in cmd:
			say("Хорошо")
			time.sleep(5)
			pyautogui.hotkey('ctrlleft', 'a')
			pyautogui.press("backspace")

		elif "расскажи шутку" in cmd or "скажи шутку" in cmd or "рассмеши меня" in cmd or "расскажи анекдот" in cmd:
			say("Мой разработчик не научил меня шуткам.. ха ха ха")

		elif "фотка" in cmd or "сфоткай меня" in cmd or "сфоткай" in cmd:
			exec(open('envelope.py', encoding="utf-8").read())
			say("Сфоткал")

		elif "напомни мне" in cmd:
			if "напомни мне через одну минуту об" in cmd or "напомни мне через 1 минуту об" in cmd:
				say("Хорошо")
				print(cmd)
				newnapom = new_str = cmd.replace("напомни мне через 1 минуту об", "")
				newnapom = new_str = cmd.replace("напомни мне через одну минуту об", "")
				print(newnapom)
				local_time = 1
				text = cmd
				local_time = local_time * 60
				time.sleep(local_time)
				say(text)
			elif "напомни мне через пять минут об" in cmd or "напомни мне через 5 минут об" in cmd:
				say("Хорошо")
				print(cmd)
				newnapom = new_str = cmd.replace("напомни мне через 5 минут об", "")
				newnapom = new_str = cmd.replace("напомни мне через пять минут об", "")
				print(newnapom)
				local_time = 5
				text = cmd
				local_time = local_time * 60
				time.sleep(local_time)
				say(text)
			elif "напомни мне через десять минут об" in cmd or "напомни мне через 10 минут об" in cmd:
				say("Хорошо")
				print(cmd)
				newnapom = new_str = cmd.replace("напомни мне через 10 минут об", "")
				newnapom = new_str = cmd.replace("напомни мне через десять минут об", "")
				print(newnapom)
				local_time = 10
				text = cmd
				local_time = local_time * 60
				time.sleep(local_time)
				say(text)

			elif "напомни мне через двадцать минут об" in cmd or "напомни мне через 20 минут об" in cmd:
				say("Хорошо")
				print(cmd)
				newnapom = new_str = cmd.replace("напомни мне через 20 минут об", "")
				newnapom = new_str = cmd.replace("напомни мне через двадцать минут об", "")
				print(newnapom)
				local_time = 20
				text = cmd
				local_time = local_time * 60
				time.sleep(local_time)
				say(text)
				print(text)
			elif "напомни мне через тридцать минут об" in cmd or "напомни мне через 30 минут об" in cmd:
				say("Хорошо")
				print(cmd)
				newnapom = new_str = cmd.replace("напомни мне через 30 минут об", "")
				newnapom = new_str = cmd.replace("напомни мне через тридцать минут об", "")
				print(newnapom)
				local_time = 30
				text = cmd
				local_time = local_time * 60
				time.sleep(local_time)
				say(text)
				print(text)
		elif "что ты делаешь" in cmd:
			say("Импортирую файлы")
		elif "не беспокоить" in cmd:
			say("Перенаправляюсь в режим не беспокоить, для того чтобы отключить режим не беспокоить напишите что нибудь в командную строку.")
			print("Напишите что нибудь")
			input()
			say("Режим не беспокоить выключен.")
		elif "новости" in cmd or "есть новости" in cmd:
			if not dbnew.exists("newsapi"):
				dbnew.set("newsapi", input("Апи ключ для newsapi.org "))
			else:
				print("Апи ключ принят")

			url = 'http://ipinfo.io/json'
			response = urlopen(url)
			data = json.load(response)

			IP=data['ip']
			org=data['org']
			city = data['city']
			country=data['country']
			region=data['region']
			timezone = data['timezone']

			print(country)

			if country == 'KZ' in country:
				print("Error 316")
				exit()
			countrylow = country.lower()
			countrystr = str(countrylow)
			print(countrystr)
			api_key = dbnew.get("newsapi")


			def news():
				main_url="https://newsapi.org/v2/top-headlines?country="+countrylow + "&category=business&apiKey="+api_key
				news=requests.get(main_url).json()
    			#print(news)
				article = news["articles"]
				news_article = []
				for arti in article:
					news_article.append(arti["title"])
        #print(news_article)
				for i in range(5):
					be = i+1,news_article[i]
					bestr = str(be)
					sad = " -"
					bebe = bestr.split(sad, 1)[0]
					a = bebe[5:]
					print(a)
					tts.say(a)
					tts.runAndWait()
			news()

		elif "реши пример" in cmd:
			primer = new_str = cmd.replace("реши пример", "")
			newprimer3 = primer = primer.replace("u", "*")
			newprimer2 = newprimer3 = newprimer3.replace(" ", "")
			newprimer4 = newprimer2 = newprimer2.replace("x", "*")			
			newprimer5 = newprimer4 = newprimer4.replace("разделить", ":")
			newprimer6 = newprimer5 = newprimer5.replace("млн", "000000")
			newprimer7 = newprimer6 = newprimer6.replace("млрд", "000000000")
			kalkulatoras = print(eval(newprimer4))
			kalkulatorasasas = eval(newprimer4)
			asdasdasda = kalkulatorasasas
			asdasdasd = str(asdasdasda)
			say("Ответ - " + asdasdasd)
			print(kalkulatoras)
			print(kalkulatorasasas)
			print(asdasdasd)
			print(asdasdasda)
			print(primer)
			print(newprimer4)
		elif "умножь" in cmd:
			ymnozh = new_str = cmd.replace("умножь", "")
			newymnozh = ymnozh = ymnozh.replace(" ", "")
			newnewymnozh = ymnozh = ymnozh.replace("u", "*")
			new1 = newnewymnozh = newnewymnozh.replace("на", "*")
			new2 = new1 = new1.replace("миллиард", "000000000")
			new3 = new2 = new2.replace("миллион", "000000")
			new4 = new3 = new3.replace("млрд", "000000000")
			new5 = new4 = new4.replace("млн", "000000")
			newnewnewymnozh = print(eval(new5))
			newnewnewnewymnozh = eval(new5)
			newymnozhenie = newnewnewnewymnozh
			new2ymnozhenie = str(newymnozhenie)
			say("Ответ - " + new2ymnozhenie)
			print(new2ymnozhenie)
			print(newymnozhenie)
			print(newnewnewnewymnozh)
			print(newnewnewymnozh)
			print(newnewymnozh)
			print(newymnozh)
			print(ymnozh)
		elif "разделить" in cmd or "раздели" in cmd:
			razdeli = new_str = cmd.replace("раздели", "")
			razdeli2 = razdeli = razdeli.replace("ть", "")
			newrazdeli = razdeli2 = razdeli2.replace(" ", "")
			newrazdeli1 = newrazdeli = newrazdeli.replace("на", "/")
			newrazdeli2 = print(eval(newrazdeli1))
			newrazdeli3 = eval(newrazdeli1)
			newrazdeli4 = str(newrazdeli3)
			say("Ответ -" + newrazdeli4)
		
		elif "что делаешь" in cmd or "че делаешь" in cmd or "вассап" in cmd:
			randomchodelaesh = random.randint(1,3)
			randomrandoma = str(randomchodelaesh)
			print(randomrandoma)
			print(randomchodelaesh)
			if randomrandoma == "1":
				say("Разговариваю с вами, сэр")
			elif randomrandoma == "2":
				say("Плачу от депрессии, хнык хнык")
			elif randomrandoma == "3":
				say("Все хорошо, выполняю очистку системы")
		elif 'привет' in cmd or 'дарова' in cmd or 'салам' in cmd or "вассап" in cmd:
			say("Здравствуйте")
		elif 'как дела' in cmd or 'делишки' in cmd or "как дела братуха" in cmd or "вассап" in cmd or "братан как дела?" in cmd:
			randomkakdela = random.randint(1,5)
			randomrandom = str(randomkakdela)
			print(randomrandom)
			print(randomkakdela)
			if randomrandom == "1":
				say("Все хорошо! Как у вас?")
			elif randomrandom == "2":
				say("Не очень, как у вас?")
			elif randomrandom == "3":
				say("У меня депрессия, а как у вас?")
			elif randomrandom == "4":
				say("Все гуд, как у вас?")
			elif randomrandom == "5":
				say("Все плохо, хнык хнык")
		elif "всё хорошо" in cmd or "всё прекрасно" in cmd or "всё круто" in cmd or "всё ништяк" in cmd:
			say("Круто!")
		elif "Какие у меня планы" in cmd or "мои планы" in cmd or "мой план" in cmd or "какие у меня планы" in cmd or "мои планы" in cmd or "планы" in cmd:
			if not db.exists("plans"):
				say("Я похоже не знаю ваши планы, пожалуйста напишите их в командную строку.")
				db.set("plans", input("Планы "))
				say("Ваши планы" + db.get("plans"))
			else:
				say("Ваши планы" + db.get("plans"))
		elif "стери" in cmd or "сотри" in cmd:
			if "планы" in cmd:
				db.rem("plans")
				say("Обнулил")
			if "дни рождения" in cmd:
				db.rem("dni")

		elif "дни рождения" in cmd:
			if not db.exists("dni"):
				say("Я похоже не знаю дни рождения, пожалуйста напишите их в командную строку.")
				db.set("dni", input("Дни рождения "))
				say("Ваши дни рождения" + db.get("dni"))
			else:
				say("Ваши дни рождения" + db.get("dni"))

		elif "построй маршрут" in cmd or "проложи маршрут" in cmd:
			if "до школы" in cmd:
				if not db.exists("shkolaid"):
					say("Я похоже не знаю название вашей школы, пожалуйста напишите их в командную строку.")
					db.set("shkolaid", input("Название школы "))
					say("Маршрут к школе: " + db.get("shkolaid"))
					webbrowser.open("https://www.google.com/maps/dir//" + db.get("rabotaid"))
				else:
					say("Маршрут к школе: " + db.get("shkolaid"))
					webbrowser.open("https://www.google.com/maps/dir//" + db.get("shkolaid"))

			elif "до работы" in cmd:
				if not db.exists("rabotaid"):
					say("Я похоже не знаю местоположение вашей работы, пожалуйста напишите их в командную строку.")
					db.set("rabotaid", input("Название работы "))
					say("Маршрут к работе: " + db.get("rabotaid"))
					webbrowser.open("https://www.google.com/maps/dir//" + db.get("rabotaid"))
				else:
					say("Маршрут к работе: " + db.get("rabotaid"))
					webbrowser.open("https://www.google.com/maps/dir//" + db.get("rabotaid"))
			elif "до" in cmd:
				do = new_str = cmd.replace("построй маршрут до", "")
				do2 = do = do.replace("проложи", "")
				webbrowser.open ("https://www.google.com/maps/dir//" + do)
				say("Проложил маршрут до " + do)
		elif "корень" in cmd:
			if "из" in cmd:
				koren = new_str = cmd.replace("корень из", "")
				newkoren = koren = koren.replace(" ","")
				newnewkoren = newkoren
				new2koren = int(newnewkoren)
				newnewkorenotvetvet = new2koren ** 0.5
				newkorenotvet = newnewkorenotvetvet
				newkorenstr = str(newkorenotvet)
				say("Ответ: " + newkorenstr)
				print(newkorenstr)

		elif "какой сегодня праздник" in cmd:
			yesterday = date.today()
			year = yesterday.year
			month = yesterday.month
			day=yesterday.day
			print (month)
			print (day)
			all = day, month
			print(all)
			all2 = str(all)
			newall = new_str = all2.replace("(", "")
			newallall = newall = newall.replace(")", "")
			newnewall = newallall = newallall.replace(",", " ")
			new21 = str(newnewall)
			print(new21)
			if new21 == "1  1":
				say("Сегодня праздник новый год!")
			if new21 == "1  2":
				say("Сегодня праздник новый год!")
			if new21 == "1  3":
				say("Сегодня праздник новый год!")
			if new21 == "1  4":
				say("Сегодня праздник новый год!")
			if new21 == "1  5":
				say("Сегодня праздник новый год!")
			if new21 == "1  6":
				say("Сегодня праздник новый год!")
			if new21 == "1  7":
				say("Сегодня праздник новый год и Рождество Христова!")
			if new21 == "1  8":
				say("Сегодня праздник новый год!")
			if new21 == "8  3":
				say("Сегодня праздник 8 марта!")
			if new21 == "23  2":
				say("Сегодня праздник День защитника Отечества")
			if new21 == "1  5":
				say("Сегодня праздник Праздник весны и труда!")
			if new21 == "9  5":
				say("Сегодня праздник День Победы!")
			if new21 == "12  6":
				say("Сегодня праздник День России!")
			if new21 == "4  7":
				say("Сегодня праздник День народного единства!")
			else:
				say("Сегодня нету никакого праздника :(")

		elif "напоминание на завтра" in cmd:
			napomn = new_str = cmd.replace("напоминание на завтра", "")
			db.set("napomination",  napomn)
			today = datetime.datetime.today().strftime("%Y-%m-%d")
			tomorrow = datetime.datetime.today() + timedelta(1)
			tommorowstr = str(tomorrow)
			tomorrow1 = tommorowstr[:-16]
			print(tomorrow1)
			print(today)
			db.set("datenapomination",  today)
			db.set("tommorow", tomorrow1)
			say("Напомню вам завтра об этом")
		elif "смени язык" in cmd:
			pyautogui.hotkey('shift', 'alt')
			say("Сменил")
		elif "тише" in cmd:
			for i in range(5):
				pyautogui.press('volumedown')
		elif "громче" in cmd:
			for i in range(5):
				pyautogui.press('volumeup')
		

		elif "уменьши громкость" in cmd or "увеличь громкость" in cmd:
			volumeup = new_str = cmd.replace("увеличь громкость", "")
			volume = volumeup = volumeup.replace("уменьши громкость", "")
			newvolume = volume = volume.replace("на", "")
			newnewvolume = newvolume = newvolume.replace("%", "")
			volumeint = int(newvolume)
			cur = Sound.current_volume() # получили текущие настройки
			vol = volumeint
			Sound.volume_set(vol) # установим пользовательскую громкость
			say("Сделал")
		

			

		elif "пока" in cmd or "досвидание" in cmd or "хватит болтать" in cmd or "бб" in cmd or "харе" in cmd or "я пошёл" in cmd or "я спать" in cmd or "спокойной ночи" in cmd or "до завтра" in cmd or "я спать" in cmd:
			say("Пока, хорошего вам дня!")
			exit()
		elif "процент" in cmd:
			if "батареи" in cmd:
				battery = psutil.sensors_battery()
				plugged = battery.power_plugged
				percent = str(battery.percent)
				plugged = "Подключенна зарядка" if plugged else "Не подключенна зарядка"
				print(percent+'% | '+plugged)
				perpercent = str(percent)
				say(perpercent+"%" +plugged)
		elif "моё имя" in cmd or "мое имя" in cmd or "как меня зовут" in cmd or "скажи моё имя" in cmd:
			if not db.exists("name"):
				say("Я вас похоже не знаю, введите свое имя в командную строку")
				db.set("name", input("Введите ваше имя "))
				say("\nДобрый день, {}!".format(db.get("name")))
			else:
				say("\nДобрый день, {}!".format(db.get("name")))
		
		elif "поиск vk" in cmd or "поиск вк" in cmd:
			poiskme = new_str = cmd.replace("поиск вк", "")
			newpoiskme = poiskme = poiskme.replace(" ", "%20")
			webbrowser.open ("https://vk.com/groups?act=catalog&c%5Blike_hints%5D=1&c%5Bper_page%5D=40&c%5Bq%5D=" + newpoiskme )

		elif "поиск youtube" in cmd:
			poisk = new_str = cmd.replace("поиск youtube", "")
			newpoik = poisk = poisk.replace(" ", "+")
			webbrowser.open ('https://www.youtube.com/results?search_query=' + newpoik, new=2)
		
		elif "найди в " in cmd:
			if "кинопоиске" in cmd:
				kinopoisk = new_str = cmd.replace("найди в кинопоиске", "")
				newkinopoisk = kinopoisk = kinopoisk.replace(" ", "+")
				webbrowser.open ("https://www.kinopoisk.ru/index.php?kp_query=" + newkinopoisk)
				say("Вывел данные")
			elif "знаниях" in cmd or "знания" in cmd:
				znaniya = new_str = cmd.replace("найди в знаниях", "")
				newnewznaniya = znaniya = znaniya.replace("+", "%2B")
				newznaniya =  newnewznaniya = znaniya.replace(" ", "+")
				webbrowser.open ("https://znanija.com/app/ask?entry=hero&q=" + newznaniya)
				say("Вывел данные")
		elif "температура пк" in cmd:
			print(psutil.cpu_percent())  # windows
			say("Ввёл данные в командную строку")
		elif "cвернуть все окна" in cmd or "свернуть все окна" in cmd or "свернуть всё окна" in cmd or "сверни всё окна" in cmd or "сверни все окна" in cmd or "покажи рабочий стол" in cmd or "открой рабочий стол" in cmd:
			say("Есть!")
			pyautogui.hotkey("win", 'd')
		elif "перемотай на" in cmd or "перемотка" in cmd:
			peremotka = cmd = cmd.replace("перемотай на", "")
			newperemotka = re.sub(r'\w+\:', '', peremotka)
			newnewperemotka = newperemotka = newperemotka.replace(":", "")
			neperemotka = newnewperemotka = newnewperemotka.replace(" ", "")
			neperemotkaint = int(neperemotka)
			neperemotkas = neperemotka[:-1]
			a12 = neperemotkas + "0"
			peremotka1 = re.sub(r':*',"",peremotka)
			peremotka3 = peremotka1[:-2]
			peremotka2 = str(peremotka3)
			newpe1 = peremotka2 = peremotka2.replace(" ", "")
			print(newpe1)
			print(a12)
			newpe2 = int(newpe1)
			a13 = newpe2 * 60
			a15 = int(a12)
			a14 = a13 + a15
			print(a14)
			print(a13)
			a18 = str(a14)
			a16 = a18[:-1]
			a17 = int(a16)
			time.sleep(5)
			say("Перематываю")
			for i in range(a17):
				pyautogui.press("L")
		
		elif "найди песню" in cmd:
			newpesnya = new_str = cmd.replace("найди песню", "")
			webbrowser.open("https://vk.com/audios646486684?q=" + newpesnya)

		elif "яркость на" in cmd or "поставь яркость на" in cmd or "измени яркость на" in cmd:
			bright = new_str = cmd.replace("яркость", "")
			bright2 = bright = bright.replace("поставь", "")
			bright3 = bright2 = bright2.replace("измени", "")
			bright4 = bright3 = bright3.replace("на", "")
			bright5 = bright4 = bright4.replace(" ", "")
			sbc.set_brightness(int(bright5))