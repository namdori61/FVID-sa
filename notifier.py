import telegram
from telegram.ext import Updater, CommandHandler
import configparser

class TelegramBot(token, id):
    def __init__(self, token, id):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.token = config["API"]["TELEGRAM_TOKEN"]
        self.id = config["API"]["TELEGRAM_CHAT_ID"]

        self.core = telegram.Bot(self.token)
        self.updater = Updater(self.token)

    def send_message(self, text):
        self.core.send_message(chat_id = self.id, text=text)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()