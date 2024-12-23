from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    """Приветствие пользователю"""
    update.message.reply_text("Привет! Я твой бот!")

def help(update: Update, context: CallbackContext):
    """Помощь по использованию бота"""
    update.message.reply_text("Команды: /start, /help")
