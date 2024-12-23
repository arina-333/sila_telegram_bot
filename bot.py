import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import re  # Для проверки даты рождения
from datetime import datetime

# Включаем логирование для получения отладочной информации
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для расчёта кармических уроков
def calculate_karma_lessons(dob: str):
    try:
        # Преобразуем строку в дату
        birth_date = datetime.strptime(dob, "%d-%m-%Y")
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year

        # Расчёт уроков по предоставленной формуле
        lesson1 = (day + month + sum([int(digit) for digit in str(year)]))
        lesson2 = lesson1 * 2 + lesson1
        lesson3 = lesson1 + lesson2

        # Если числа больше 22, складываем их цифры
        def reduce_to_22(number):
            while number > 22:
                number = sum([int(digit) for digit in str(number)])
            return number

        lesson1 = reduce_to_22(lesson1)
        lesson2 = reduce_to_22(lesson2)
        lesson3 = reduce_to_22(lesson3)

        return lesson1, lesson2, lesson3
    except Exception as e:
        logger.error(f"Error calculating karma lessons: {e}")
        return None

# Асинхронная функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение при вызове команды /start"""
    welcome_text = "Привет! Я твой бот для расчёта кармических уроков и проработки задач."
    keyboard = [[InlineKeyboardButton("Расчитать мои уроки", callback_data='calculate_lessons')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Асинхронная функция для обработки команды /help
async def help_command(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение с инструкцией при вызове команды /help"""
    help_text = (
        "Этот бот может помочь тебе рассчитать кармические уроки. "
        "Ты просто вводишь свою дату рождения (в формате ДД-ММ-ГГГГ), и я покажу тебе твои уроки."
        " Также ты сможешь принять участие в проработке этих уроков, получая задания каждую неделю."
    )
    await update.message.reply_text(help_text)

# Асинхронная функция для обработки команды /info
async def info(update: Update, context: CallbackContext) -> None:
    """Отправляет информацию о системе расчета при вызове команды /info"""
    info_text = (
        "Моя система расчета матрицы судьбы основана на числах, которые получают "
        "люди в зависимости от их даты рождения. Ты можешь рассчитать кармические уроки, чтобы понять "
        "свои жизненные задачи."
    )
    await update.message.reply_text(info_text)

# Асинхронная функция для обработки ввода даты рождения
async def handle_birthday(update: Update, context: CallbackContext) -> None:
    """Обрабатывает текстовое сообщение с датой рождения и рассчитывает кармические уроки"""
    dob = update.message.text.strip()
    
    # Проверка формата даты
    if re.match(r"\d{2}-\d{2}-\d{4}", dob):
        lessons = calculate_karma_lessons(dob)
        if lessons:
            lesson1, lesson2, lesson3 = lessons
            await update.message.reply_text(
                f"Ваши кармические уроки:\nУрок 1: {lesson1}\nУрок 2: {lesson2}\nУрок 3: {lesson3}\n"
                "Хотите начать проработку? Нажмите 'Да' для начала или 'Нет' для выхода."
            )
        else:
            await update.message.reply_text("Произошла ошибка при расчете уроков. Попробуйте снова.")
    else:
        await update.message.reply_text("Пожалуйста, введите дату рождения в формате ДД-ММ-ГГГГ.")

# Асинхронная функция для начала проработки кармических уроков
async def start_working_on_lessons(update: Update, context: CallbackContext) -> None:
    """Начинает процесс проработки кармических уроков"""
    keyboard = [
        [InlineKeyboardButton("Оплатить залог 1000 рублей", callback_data='pay_deposit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Для начала проработки уроков, необходимо оплатить залог в размере 1000 рублей.",
        reply_markup=reply_markup
    )

# Асинхронная функция для обработки кнопки оплаты
async def handle_payment(update: Update, context: CallbackContext) -> None:
    """Обрабатывает кнопку оплаты"""
    await update.message.reply_text("Спасибо за оплату! Начинаем проработку кармических уроков.")

# Обработка callback-запросов (например, нажатие кнопок)
async def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "calculate_lessons":
        await update.callback_query.message.reply_text("Введите вашу дату рождения в формате ДД-ММ-ГГГГ.")
    elif query.data == "pay_deposit":
        await update.callback_query.message.reply_text("Спасибо за оплату! Начинаем проработку кармических уроков.")

# Главная асинхронная функция, которая запускает бота
async def main() -> None:
    """Основная функция для запуска бота"""
    TOKEN = 'your-telegram-bot-token'  # Замените на свой токен

    # Создаем асинхронное приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))

    # Регистрируем обработчик ввода даты рождения
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birthday))

    # Регистрируем обработчики кнопок
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Запуск бота (уже внутри цикла событий)
    await application.run_polling()

# Запуск асинхронной функции
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
