from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Асинхронная функция для команды /start
async def start(update: Update, context: CallbackContext):
    """Приветствие пользователю"""
    await update.message.reply_text("Привет! Я твой бот!")

# Асинхронная функция для команды /help
async def help(update: Update, context: CallbackContext):
    """Помощь по использованию бота"""
    await update.message.reply_text("Команды: /start, /help")

# Основная асинхронная функция для запуска бота
async def main() -> None:
    """Основная функция для запуска бота"""
    TOKEN = 'your-telegram-bot-token'  # Замените на свой токен

    # Создаем асинхронное приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # Запуск бота (уже внутри цикла событий)
    await application.run_polling()

# Запуск асинхронной функции
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
