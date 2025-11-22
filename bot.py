import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# --- Твой токен ---
TOKEN = "8321577382:AAF8sPv8N41WUk1Sa8ZMbPIn6sQznkGzk6Q"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Команды RP без наращивания (а) ---
all_commands = {
    "обнять": {"emoji": "🤗", "past": "обнял"},
    "поцеловать": {"emoji": "💋", "past": "поцеловал"},
    "дать пять": {"emoji": "🖐️", "past": "дал пять"},
    "испугать": {"emoji": "😱", "past": "испугал"},
    "извиниться": {"emoji": "🙏", "past": "извинился"},
    "куснуть": {"emoji": "🦷", "past": "куснул"},
    "пнуть": {"emoji": "👟", "past": "пнул"},
    "ударить": {"emoji": "🥊", "past": "ударил"},
    "похвалить": {"emoji": "👏", "past": "похвалил"},
    "погладить": {"emoji": "🫶", "past": "погладил"},
    "поздравить": {"emoji": "🎉", "past": "поздравил"},
    "пожать руку": {"emoji": "🤝", "past": "пожал руку"},
    "шлёпнуть": {"emoji": "🍑", "past": "шлёпнул"},
    "расстрелять": {"emoji": "🔫", "past": "расстрелял"},
    "сжечь": {"emoji": "🔥", "past": "сжёг"},
    "пригласить на чаёк": {"emoji": "🍵", "past": "пригласил на чаёк"},
    "понюхать": {"emoji": "👃", "past": "понюхал"},
    "покормить": {"emoji": "🍽️", "past": "покормил"},
    "потрогать": {"emoji": "✋", "past": "потрогал"},
    "ущипнуть": {"emoji": "🤏", "past": "ущипнул"},
    "связать": {"emoji": "🪢", "past": "связал"},
    "повесить": {"emoji": "🪤", "past": "повесил"},
    "уничтожить": {"emoji": "💣", "past": "уничтожил"},
    "взорвать": {"emoji": "💥", "past": "взорвал"},
    "щекотать": {"emoji": "😆", "past": "пощекотал"},
    "арестовать": {"emoji": "👮", "past": "арестовал"},
    "рассмешить": {"emoji": "😂", "past": "рассмешил"},
    "ушатать": {"emoji": "🧱", "past": "ушатал"},
    "порвать": {"emoji": "🧻", "past": "порвал"},
    "выпороть": {"emoji": "🩸", "past": "выпорол"},
    "сделать большой подарок": {"emoji": "🎁", "past": "сделал большой подарок"},
    "устроить сюрприз": {"emoji": "🎊", "past": "устроил сюрприз"},
    "подарить шоколадку": {"emoji": "🍫", "past": "подарил шоколадку"},
    "поговорить по душам": {"emoji": "💞", "past": "поговорил по душам"},
    "сходить в кино": {"emoji": "🎬", "past": "сходил в кино"},
    "пригласить погулять": {"emoji": "🌆", "past": "пригласил погулять"},
    "сделать комплимент": {"emoji": "🌹", "past": "сделал комплимент"}
}

# --- HELP в мобильном формате ---
def format_help():
    commands_text = "\n".join([f"{v['emoji']} {k}" for k,v in all_commands.items()])
    return f"""
🎮 <b>Доступные RP-команды:</b>

<code>
{commands_text}
</code>

<b>💡 Как использовать:</b>
• Ответить на сообщение ОДНОЙ командой
• Или написать: команда @username
Пример: обнять @username
"""

@dp.message(Command("help", prefix="!"))
async def help_cmd(message: Message):
    await message.answer(format_help(), parse_mode="HTML")

# --- нормализация 'ё' ---
def normalize(text: str):
    return text.replace("ё", "е")

# --- RP действия с эмодзи и прошедшим временем ---
@dp.message()
async def rp_action(message: Message):
    try:
        if not message.text:
            return

        text = message.text.lower().strip()
        norm = normalize(text)

        # === Ответ на сообщение ===
        if message.reply_to_message:
            for cmd, data in all_commands.items():
                if normalize(cmd) == norm:
                    actor = message.from_user
                    target = message.reply_to_message.from_user
                    await message.reply(
                        f"{data['emoji']} Пользователь @{actor.username or actor.first_name} {data['past']} @{target.username or target.first_name} {data['emoji']}"
                    )
                    return

        # === Команда рядом с упоминанием ===
        if message.entities:
            for entity in message.entities:
                if entity.type == "mention":
                    mention = message.text[entity.offset:entity.offset + entity.length]
                    for cmd, data in all_commands.items():
                        if normalize(cmd) in norm:
                            actor = message.from_user
                            await message.reply(
                                f"{data['emoji']} Пользователь @{actor.username or actor.first_name} {data['past']} {mention} {data['emoji']}"
                            )
                            return

    except Exception as e:
        logging.error(e)

# --- Запуск бота ---
async def main():
    logging.info("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())