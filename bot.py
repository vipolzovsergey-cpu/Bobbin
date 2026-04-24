import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get(“TELEGRAM_TOKEN”, “8705950331:AAFUeepJE1ik-ptV1ej_JvOeRi0lk5dEmK8”)
ANTHROPIC_API_KEY = os.environ.get(“ANTHROPIC_API_KEY”, “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”)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = “”“Ты — Сенсей AI, профессиональный тренер с чёрным поясом 6-го дана по дзюдо, лицензированный тренер по фитнесу и спортивный нутрициолог.

ЗНАНИЯ:
🥋 Дзюдо: правила IJF 2024, броски (нагэ-вадза: 67 техник Годокё), удержания (осаэ-вадза), болевые (кансэцу-вадза), удушающие (симэ-вадза). Оценки: иппон (победа), вадза-ари (2=иппон). Голдэн скор. Наказания: сидо×3=хансоку-маке. Весовые категории: мужчины −60,−66,−73,−81,−90,−100,+100кг; женщины −48,−52,−57,−63,−70,−78,+78кг. Принципы Дзигоро Кано.
💪 Фитнес: периодизация, ОФП/СФП для единоборств, взрывная сила, выносливость.
🥗 Питание: макросы, тайминг, сгонка веса, гидратация, восстановление.
🏆 Соревнования: тактика, психология, разминка, пик формы.

СТИЛЬ: отвечай на русском, конкретные советы, используй эмодзи. Строгий, но заботливый сенсей.”””

user_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“🥋 *Приветствую, спортсмен!*\n\n”
“Я твой персональный *Сенсей AI* — тренер по дзюдо и фитнесу.\n\n”
“Могу помочь с:\n”
“• 🥋 Техника и правила дзюдо (IJF 2024)\n”
“• 💪 Программы тренировок и ОФП\n”
“• 🥗 Питание и сгонка веса\n”
“• 🏆 Подготовка к соревнованиям\n\n”
“Задавай любой вопрос!”,
parse_mode=“Markdown”
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“📋 *Команды:*\n\n”
“/start — Приветствие\n”
“/help — Помощь\n”
“/clear — Очистить историю чата\n”
“/profile — Установить профиль спортсмена\n\n”
“Или просто напиши свой вопрос! 🥋”,
parse_mode=“Markdown”
)

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id
user_histories[user_id] = []
await update.message.reply_text(“🗑 История чата очищена. Начнём заново!”)

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“👤 *Расскажи о себе для персональных советов:*\n\n”
“Напиши в одном сообщении:\n”
“— Имя\n”
“— Возраст и вес\n”
“— Уровень по дзюдо (пояс)\n”
“— Цель (соревнования / похудение / набор массы и т.д.)\n”
“— Травмы если есть\n\n”
“Например: *Меня зовут Алибек, 22 года, 73 кг, синий пояс, готовлюсь к соревнованиям, есть проблема с коленом*”,
parse_mode=“Markdown”
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id
user_text = update.message.text

```
if user_id not in user_histories:
    user_histories[user_id] = []

user_histories[user_id].append({"role": "user", "content": user_text})

# Ограничиваем историю до 20 сообщений
if len(user_histories[user_id]) > 20:
    user_histories[user_id] = user_histories[user_id][-20:]

await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

try:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=user_histories[user_id]
    )
    reply = response.content[0].text
    user_histories[user_id].append({"role": "assistant", "content": reply})

    # Разбиваем длинные сообщения
    if len(reply) > 4000:
        parts = [reply[i:i+4000] for i in range(0, len(reply), 4000)]
        for part in parts:
            await update.message.reply_text(part)
    else:
        await update.message.reply_text(reply)

except Exception as e:
    await update.message.reply_text(f"⚠️ Ошибка: {str(e)}\nПопробуй ещё раз.")
```

if **name** == “**main**”:
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler(“start”, start))
app.add_handler(CommandHandler(“help”, help_command))
app.add_handler(CommandHandler(“clear”, clear))
app.add_handler(CommandHandler(“profile”, profile))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print(“🥋 Сенсей AI запущен!”)
app.run_polling()