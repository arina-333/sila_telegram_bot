const { Bot, InlineKeyboard } = require("grammy");
const { Keyboard } = require("@grammyjs/keyboard");
const moment = require("moment");

// Токен бота
const bot = new Bot("7754998709:AAHf8cZmQocHwmy4p4CMJxll-d5bAvyymv0");

// Функция для расчета кармических уроков
function calculateKarmaLessons(dob) {
    try {
        const birthDate = moment(dob, "DD.MM.YYYY");
        if (!birthDate.isValid()) throw new Error("Invalid date format");

        const day = birthDate.date();
        const month = birthDate.month() + 1; // месяц от 0 до 11
        const year = birthDate.year();

        let lesson1 = day + month + year.toString().split("").reduce((a, b) => a + Number(b), 0);
        let lesson2 = lesson1 * 2 + lesson1;
        let lesson3 = lesson1 + lesson2;

        const reduceTo22 = (number) => {
            while (number > 22) {
                number = number
                    .toString()
                    .split("")
                    .reduce((a, b) => a + Number(b), 0);
            }
            return number;
        };

        return [reduceTo22(lesson1), reduceTo22(lesson2), reduceTo22(lesson3)];
    } catch (e) {
        console.error("Error calculating karma lessons:", e);
        return null;
    }
}

// Команда /start
bot.command("start", async (ctx) => {
    const userName = ctx.from?.first_name || "друг";
    const welcomeText = `Привет, ${userName}! Добро пожаловать в матрицу судьбы!`;

    const keyboard = new InlineKeyboard()
        .text("Помощь", "help").row()
        .text("Информация о системе", "info").row()
        .text("Рассчитать кармические уроки", "calculate").row()
        .text("Начать проработку уроков", "start_working");

    await ctx.reply(welcomeText, { reply_markup: keyboard });
});

// Обработка помощи
bot.callbackQuery("help", async (ctx) => {
    const helpText = "Этот бот поможет тебе рассчитать кармические уроки.\n" +
        "Для начала введи свою дату рождения в формате ДД.ММ.ГГГГ.";
    await ctx.answerCallbackQuery();
    await ctx.editMessageText(helpText);
});

// Информация о системе
bot.callbackQuery("info", async (ctx) => {
    const infoText = "Моя система расчета матрицы судьбы поможет тебе понять кармические уроки и направления для развития.";
    await ctx.answerCallbackQuery();
    await ctx.editMessageText(infoText);
});

// Расчет кармических уроков
bot.callbackQuery("calculate", async (ctx) => {
    await ctx.answerCallbackQuery();
    await ctx.editMessageText("Введите свою дату рождения в формате ДД.ММ.ГГГГ.");
});

// Обработка ввода даты рождения
bot.on("message:text", async (ctx) => {
    const dob = ctx.message.text;
    if (!moment(dob, "DD.MM.YYYY", true).isValid()) {
        await ctx.reply("Неправильный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.");
        return;
    }

    const lessons = calculateKarmaLessons(dob);
    if (lessons) {
        const [lesson1, lesson2, lesson3] = lessons;
        const resultText = `Ваши кармические уроки:\nУрок 1: ${lesson1}\nУрок 2: ${lesson2}\nУрок 3: ${lesson3}\n` +
            "Готовы начать проработку? Нажмите кнопку ниже.";

        const keyboard = new InlineKeyboard().text("Начать проработку", "start_working");
        await ctx.reply(resultText, { reply_markup: keyboard });
    } else {
        await ctx.reply("Произошла ошибка при расчете уроков. Попробуйте снова.");
    }
});

// Начало проработки уроков
bot.callbackQuery("start_working", async (ctx) => {
    const keyboard = new InlineKeyboard()
        .text("Оплатить залог 1000 рублей", "pay_deposit").row()
        .text("Вернуться в меню", "menu");

    await ctx.answerCallbackQuery();
    await ctx.editMessageText(
        "Для начала проработки уроков необходимо оплатить залог 1000 рублей.",
        { reply_markup: keyboard }
    );
});

// Обработка оплаты
bot.callbackQuery("pay_deposit", async (ctx) => {
    await ctx.answerCallbackQuery();
    await ctx.editMessageText("Спасибо за оплату! Начинаем проработку уроков.");
});

// Возврат в меню
bot.callbackQuery("menu", async (ctx) => {
    await ctx.answerCallbackQuery();
    await ctx.editMessageText("Что ты хочешь сделать?", {
        reply_markup: new InlineKeyboard()
            .text("Помощь", "help").row()
            .text("Информация о системе", "info").row()
            .text("Рассчитать кармические уроки", "calculate").row()
            .text("Начать проработку уроков", "start_working"),
    });
});

// Запуск бота
bot.start();
