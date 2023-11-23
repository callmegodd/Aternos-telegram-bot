import os
import time
from datetime import datetime
from python_aternos import Client
import telebot
from telebot import types
from background import keep_alive

keep_alive()
ATERNOS_NAME = os.environ['ATERNOS_NAME']
ATERNOS_PASSWD = os.environ['ATERNOS_PASSWD']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TELEGRAM_TOKEN)
at = Client.from_credentials(ATERNOS_NAME, ATERNOS_PASSWD)
at.save_session()
server = 'N/S'
named_tuple = time.localtime()
time_string = 'N/S'


def setup_server():
 serv = Client.restore_session().list_servers()[0]
 serv.start()
 serv.confirm()


def server_state():
 serv = Client.restore_session().list_servers()[0]
 return f"Состояние сервера: {serv.status}\nАдрес сервера: {serv.address}\nВерсия сервера:" \
        f" {serv.version}\nОнлайн: {serv.players_count} из {serv.slots}"


@bot.message_handler(commands=['start'])
def start(message):
 markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
 button = types.KeyboardButton("Состояние Java сервера.")
 button2 = types.KeyboardButton("Запустить Java сервер.")
 button3 = types.KeyboardButton("Проверка работоспобности бота")
 markup.add(button, button2, button3)
 bot.send_message(message.chat.id,
                  f"Время отклика сервера ~ {server} секунд",
                  reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
 global server
 global time_string
 if message.text == "Состояние Java сервера.":
  try:
   start1 = time.time()
   bot.send_message(message.chat.id, server_state())
   server = round(time.time() - start1, 3)
   time_string = datetime.now()
  except (Exception, ) as err:
   bot.send_message(message.chat.id,
                    f"Обработчик исключений выдал ошибку: {err}")

 elif message.text == "Запустить Java сервер.":
  try:
   startt = time.time()
   setup_server()
   bot.send_message(message.chat.id, f"Запускаю сервер. \n{server_state()}")
   server = round(time.time() - startt, 3)
   time_string = datetime.now()
  except (Exception, ) as err:
   bot.send_message(message.chat.id,
                    f"Обработчик исключений выдал ошибку: {err}")
 else:
  startt = time.time()
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  button = types.KeyboardButton("Состояние Java сервера.")
  button2 = types.KeyboardButton("Запустить Java сервер.")
  button3 = types.KeyboardButton("Проверка рабоспобности бота")
  markup.add(button, button2, button3)
  bot.send_message(message.chat.id,
                   "Производится расчёт...",
                   reply_markup=markup)
  bot.send_message(
   message.chat.id,
   f"Скорость ответа: {round(time.time() - startt, 3)} секунд. \nСкорость отклика сервера: {server} секунд. Последняя проверка: {time_string} UTC"
  )


bot.polling(none_stop=True)