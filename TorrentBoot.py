import telebot
import configBot
import subprocess
import os
import phrases
import requests

from functools import wraps

from telebot import types
bot = telebot.TeleBot(configBot.TOKEN)
document_dict = {}

torntImg = open('torrent1.webp','rb')

download_path_ext_mov = "/media/pi/HugeTom/Movies"
download_path_ext_oth = "/media/pi/HugeTom/torrent"
download_path_home = "/home/pi/Downloads/"

class Document:
    def __init__(self, name):
        self.name = name


@bot.message_handler(func=lambda message: message.chat.id == int(configBot.MyIDS) , commands=["start"])
def welcome(message):


	#keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton(phrases.dTfTorrent) #("Отправить торрент файл")
	item2 = types.KeyboardButton(phrases.dTfLink) #("Отправить ссылку на торрент")
	item3 = types.KeyboardButton(phrases.dFfLink) #("Отправить ссылку на файл")

	markup.add(item1,item2,item3)
	bot.send_message(message.from_user.id, "Приветствую повелитель! Что прикажете делать?", reply_markup=markup)

#методы обработки сообщений
@bot.message_handler(func=lambda message: message.chat.id == int(configBot.MyIDS), content_types=['text'])

def messgHand(message):
	if message.text == phrases.dTfTorrent:
		bot.send_photo(message.chat.id,torntImg)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Внеш. Movies file" )
		item2 = types.KeyboardButton("Внеш. Torrents file")
		item3 = types.KeyboardButton("Home file")
		markup.add(item1, item2, item3)
		msg = bot.reply_to(message, "Выбери куда скачать файл", reply_markup=markup)
	elif message.text == phrases.dTfLink:
		msg = bot.reply_to(message,"Скинь ссылку на торрент вида https://torrent.com/tor.torrent")
		bot.register_next_step_handler(msg,download_torrent_link)
	elif message.text == phrases.dFfLink:
		msg = bot.reply_to(message, "Скинь мне ссылку на загрузку..")
		bot.register_next_step_handler(msg,download_file_link)
	elif message.text == "Внеш. Movies file":




#@bot.message_handler(funk=lambda message: message.chat.id ==
#int(configBot.MyIDS), content_types=['document'])
def DocHanld(message):
	if message.content_type == 'document':
		download_torrent_Ffile(message)
	else:
	   bot.reply_to(message,"И зачем оно мне надо??")

#Методы обработки запросов
def download_file_link(message):
		os.system("kget " + message.text)
		bot.send_message(message.chat.id, "Загрузка началась")

filename_last = ""

def download_torrent_Ffile(message, dwnpath):
		if message.content_type == "document":
			file_size = message.document.file_size
			file_name = message.document.file_name
			document = Document(file_name)
			document_dict[str(message.from_user.id)] = document

			file_info = bot.get_file(message.document.file_id)
			filelink_hand = ("https://api.telegram.org/file/bot" + configBot.TOKEN + "/" + file_info.file_path)	
			r = requests.get(filelink_hand)
			with open("cache\\"+file_name, 'wb') as f:
				f.write(r.content)
			bot.send_message(message.from_user.id ,str(file_name) + " загружен.")
			os.system('qbittorrent --save-path="'+dwnpath+'" '+"cache\\"+file_name)
			bot.send_message(message.from_user.id, "Торрент поставлен на загрузку в папку "+dwnpath)
			

def download_torrent_link(message ):
	os.system("qbittorrent " + message.text)
	bot.send_message(message.from_user.id, "Файл поставлен на загрузку")

def ask_for_coms(message):
	bot.send_message(message.from_user.id,"Command list:\n /sendtorrentlink - just send link for a torrent file to download it\n /sendtorrent - send torrent file to download\n /sendfilelink - send any link to a file to download")

# RUN
bot.polling(none_stop=True)

#Запоминаем последнее присланное сообщение в переменную
#При получении следующего сообщения (если это не файл) проверяем какое было последнее сообщение и действуем исходя из того что оно должно сделать
#Если в сообщении файл, то обрабатываем его только тогда если последнее сообщение равно отправить файл торрента.
#
#
#
#
#
