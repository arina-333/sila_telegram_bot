import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Функции для команд
def start(update: Update, context: CallbackContext):
    """Приветствие и отправка видео."""
    chat_id = update.message.chat_id
    update.message.reply_text(
        "Привет! Я помогу тебе рассчитать твои кармические уроки и начать их проработку."
        "\nДля начала введи дату рождения в формате ДД.ММ.ГГГГ."
    )
    context.bot.send_video(chat_id=chat_id, video=open("welcome_video.mp4", "rb"))

def help_command(update: Update, context: CallbackContext):
    """Справочная информация."""
    update.message.reply_text(
        "/start - Начать работу с ботом\n"
        "/help - Помощь\n"
        "/info - Узнать обо мне\n"
        "/lessons - Рассчитать уроки\n"
        "/tasks - Текущие задания\n"
        "/progress - Мой прогресс\n"
        "/payment - Оплатить залог\n"
        "/charity - Узнать о благотворительности\n"
        "/remind - Напомнить о задании\n"
        "/cancel - Отменить участие\n"
        "/feedback - Оставить отзыв\n"
        "/restart - Начать заново"
    )

def info(update: Update, context: CallbackContext):
    """Информация о системе расчета."""
    update.message.reply_text(
        "Описание системы расчета будет здесь. "
        "Это временная заглушка для команды /info."
    )

def calculate_lessons(update: Update, context: CallbackContext):
    """Рассчитываем уроки по введенной дате."""
    try:
        date = update.message.text.strip()
        day, month, year = map(int, date.split("."))
        
        # Расчеты
        first_lesson = sum(map(int, f"{day}{month}{year}"))
        first_lesson = first_lesson if first_lesson <= 22 else sum(map(int, str(first_lesson)))
        
        second_lesson = first_lesson * 2 + first_lesson
        second_lesson = second_lesson if second_lesson <= 22 else sum(map(int, str(second_lesson)))
        
        third_lesson = first_lesson + second_lesson
        third_lesson = third_lesson if third_lesson <= 22 else sum(map(int, str(third_lesson)))
        
        # Сохраняем уроки в контекст пользователя
        context.user_data['lessons'] = {
            "lesson_1": first_lesson,
            "lesson_2": second_lesson,
            "lesson_3": third_lesson,
        }
        
        # Ответ пользователю
        update.message.reply_text(
            f"Ваши кармические уроки:\n"
            f"Урок 1: {first_lesson} — Описание будет здесь.\n"
            f"Урок 2: {second_lesson} — Описание будет здесь.\n"
            f"Урок 3: {third_lesson} — Описание будет здесь.\n"
            "Перейдите к команде /tasks, чтобы начать работать над заданиями."
        )
    except Exception as e:
        update.message.reply_text("Ошибка! Пожалуйста, введите дату рождения в формате ДД.ММ.ГГГГ.")

def tasks(update: Update, context: CallbackContext):
    """Показ текущих заданий."""
    lessons = context.user_data.get('lessons')
    if not lessons:
        update.message.reply_text("Пожалуйста, сначала рассчитайте свои уроки с помощью команды /lessons.")
        return
    
    update.message.reply_text(
        "Ваши текущие задания:\n"
        f"Урок 1: Задание для урока {lessons['lesson_1']} — Заглушка.\n"
        f"Урок 2: Задание для урока {lessons['lesson_2']} — Заглушка.\n"
        f"Урок 3: Задание для урока {lessons['lesson_3']} — Заглушка.\n"
        "Следуйте инструкциям и выполняйте задания!"
    )

def progress(update: Update, context: CallbackContext):
    """Отображение прогресса пользователя."""
    update.message.reply_text("Ваш текущий прогресс: 0 выполнено, 4 осталось. Это временная заглушка.")

def payment(update: Update, context: CallbackContext):
    """Информация об оплате."""
    update.message.reply_text(
        "Для участия необходимо внести залог 1000 рублей. Это временная заглушка."
        "Нажмите кнопку ниже, чтобы оплатить.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Оплатить", url="https://example.com/payment")]
        ])
    )

def charity(update: Update, context: CallbackContext):
    """Информация о благотворительности."""
    update.message.reply_text(
        "Описание благотворительности будет здесь. Это временная заглушка."
    )

def cancel(update: Update, context: CallbackContext):
    """Отмена участия."""
    update.message.reply_text("Ваше участие отменено. Это временная заглушка.")

def feedback(update: Update, context: CallbackContext):
    """Оставить отзыв."""
    update.message.reply_text("Форма для отзыва будет здесь. Это временная заглушка.")

def restart(update: Update, context: CallbackContext):
    """Сброс прогресса и начало заново."""
    context.user_data.clear()
    update.message.reply_text("Ваш прогресс сброшен. Это временная заглушка.")

# Основной код
def main():
    TOKEN = 7754998709:AAHf8cZmQocHwmy4p4CMJxll-d5bAvyymv0 
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Обработка команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("lessons", calculate_lessons))
    dp.add_handler(CommandHandler("tasks", tasks))
    dp.add_handler(CommandHandler("progress", progress))
    dp.add_handler(CommandHandler("payment", payment))
    dp.add_handler(CommandHandler("charity", charity))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CommandHandler("feedback", feedback))
    dp.add_handler(CommandHandler("restart", restart))

    # Обработка текста (расчет уроков)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, calculate_lessons))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()



