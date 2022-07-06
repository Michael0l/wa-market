from flask import Flask
from telebot import TeleBot
import config



app = Flask(__name__, static_folder='web_app/static', template_folder='web_app/templates')
bot = TeleBot(config.BOT_TOKEN, parse_mode="html", skip_pending=True)

