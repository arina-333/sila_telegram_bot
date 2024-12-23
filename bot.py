import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from telegram.constants import ParseMode

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "7754998709:AAHf8cZmQocHwmy4p4CMJxll-d5bAvyymv0"

# Функция старта
async def start(update: Update, context: CallbackContext) -> None:
    # Приветствие и отправка приветственного видео
    user_name = update.message.from_user.first_name
    await update.message.reply(f"Привет, {user_name}!\nДобро пожаловать в матрицу судьбы!")
    # Здесь можно отправить видео (например, с ID видео в Telegram)
    # await update.message.reply_video(video_id)

    # Меню с кнопками
    keyboard = [
        [InlineKeyboardButton("Помощь", callback_data='help')],
        [InlineKeyboardButton("Информация о системе", callback_data='info')],
        [InlineKeyboardButton("Рассчитать кармические уроки", callback_data='calculate')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Что ты хочешь сделать?', reply_markup=reply_markup)

# Функция помощи
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply("Я помогу тебе рассчитать кармические уроки.\n"
                               "Сначала введи свою дату рождения.")

# Информация о системе расчета
async def info(update: Update, context: CallbackContext) -> None:
    info_text = (
        "Моя система расчета матрицы судьбы поможет тебе понять кармические уроки "
        "и направления для личностного роста. Я разработала эту систему, чтобы помочь людям "
        "раскрыть свой потенциал и научиться преодолевать трудности жизни."
    )
    await update.message.reply_text(info_text)

# Функция для расчета кармических уроков
async def calculate(update: Update, context: CallbackContext) -> None:
    await update.message.reply("Пожалуйста, введи свою дату рождения в формате ДД.ММ.ГГГГ.")

# Функция для обработки введенной даты рождения
async def handle_birthday(update: Update, context: CallbackContext) -> None:
    try:
        date_of_birth = update.message.text
        # Преобразуем дату в список чисел
        day, month, year = map(int, date_of_birth.split('.'))
        # Применяем формулу расчета уроков
        lesson_1 = day + month + sum(map(int, str(year)))
        lesson_2 = 2 * lesson_1 + lesson_1
        lesson_3 = lesson_1 + lesson_2
        # Применяем правило для чисел больше 22
        lesson_1 = sum(map(int, str(lesson_1))) if lesson_1 > 22 else lesson_1
        lesson_2 = sum(map(int, str(lesson_2))) if lesson_2 > 22 else lesson_2
        lesson_3 = sum(map(int, str(lesson_3))) if lesson_3 > 22 else lesson_3

        # Отправляем результаты
        result_text = f"Твои кармические уроки:\nУрок 1: {lesson_1}\nУрок 2: {lesson_2}\nУрок 3: {lesson_3}"
        await update.message.reply_text(result_text)
    except Exception as e:
        await update.message.reply_text("Неправильный формат даты. Попробуй снова.")
        logger.error(f"Error processing date: {e}")

# Функция для обработки кнопок
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        await help_command(update, context)
    elif query.data == 'info':
        await info(update, context)
    elif query.data == 'calculate':
        await calculate(update, context)

# Основная функция
async def main():
    # Создание приложения с токеном
    application = Application.builder().token(TOKEN).build()

    # Хендлеры
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birthday))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
