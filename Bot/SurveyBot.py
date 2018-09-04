import telegram
from telegram.ext import Updater
import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters)
from Bot import Survey

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token='661947800:AAG95ml8ys3o-A_s8SMGzeDw09TYeKIKp98')
dispatcher = updater.dispatcher

APIURL = "http://psi.rc.center/psi/index.php?r=admin/remotecontrol"
user = 'admin'
password = 'password'
s = Survey(APIURL, user, password)

s.get_session_key()
surveys = s.list_surveys()


def start(bot, update):
    custom_keyboard = [['Список опросов']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="Команды /list", reply_markup=reply_markup)


def text(bot, update):
    message = update.message.text

    if message == "Список опросов":
        list_surveys(bot, update)


def list_surveys(bot, update):

    custom_keyboard = []
    for survey in surveys:
        custom_keyboard.append([survey["surveyls_title"]])

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="Список опросов:", reply_markup=reply_markup)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

list_handler = CommandHandler('list', list_surveys)
dispatcher.add_handler(list_handler)

list_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(list_handler)

updater.start_polling()