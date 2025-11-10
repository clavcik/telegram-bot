import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError
import asyncio
import os

# Устанавливаем aiogram если не установлен (для Render)
try:
    from aiogram import Bot
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiogram==3.10.0"])
    from aiogram import Bot, Dispatcher, types
    from aiogram.types import Message
    from aiogram.filters import Command
    from aiogram.exceptions import TelegramForbiddenError

# Получаем токен из переменных окружения
token = os.getenv("BOT_TOKEN")

if not token:
    logging.error("BOT_TOKEN не установлен!")
    exit(1)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

# --- Список всех команд ---
all_commands = {
    "обнять": "🤗", "поцеловать": "💋", "дать пять": "🖐️", "испугать": "😱", "извиниться": "🙏", "куснуть": "🦷",
    "пнуть": "👟", "ударить": "🥊", "похвалить": "👏", "погладить": "🫶", "поздравить": "🎉", "пожать руку": "🤝",
    "шлёпнуть": "🍑", "расстрелять": "🔫", "сжечь": "🔥", "пригласить на чаёк": "🍵", "понюхать": "👃", "покормить": "🍽️",
    "потрогать": "✋", "ущипнуть": "🤏", "связать": "🪢", "повесить": "🪤", "уничтожить": "💣", "взорвать": "💥",
    "щекотать": "😆", "арестовать": "👮", "рассмешить": "😂", "ушатать": "🧱", "порвать": "🧻", "выпороть": "🩸",
    "сделать большой подарок": "🎁", "устроить сюрприз": "🎊", "подарить шоколадку": "🍫", "поговорить по душам": "💞",
    "сходить в кино": "🎬", "пригласить погулять": "🌆", "сделать комплимент": "🌹"
}

# --- Функция для замены ё на е ---
def normalize_text(text):
    """Заменяет ё на е в тексте для унификации"""
    return text.replace('ё', 'е')

# --- Красивое форматирование списка команд ---
def format_commands_list():
    commands_list = list(all_commands.keys())
    middle = len(commands_list) // 2
    
    left_column = commands_list[:middle]
    right_column = commands_list[middle:]
    
    text = "🎮 <b>Доступные рп-команды:</b>\n\n"
    
    # Создаем две колонки с широким расстоянием
    max_len = max(len(left_column), len(right_column))
    
    for i in range(max_len):
        line = ""
        if i < len(left_column):
            line += f"• {left_column[i]:<25}"
        else:
            line += " " * 28
            
        if i < len(right_column):
            line += f"• {right_column[i]}"
        
        text += line + "\n"
    
    text += "\n💡 <b>Как использовать:</b>\n"
    text += "Напиши команду в ответ на сообщение пользователя\n"
    text += "Пример: <code>обнять</code> (в ответ на сообщение)\n\n"
    text += "✨ Бот автоматически отреагирует на любую команду из списка!"
    
    return text

# --- Команда !help ---
@dp.message(Command('help', prefix='!'))
async def help_command(message: Message):
    try:
        text = format_commands_list()
        await message.answer(text, parse_mode='HTML')
    except TelegramForbiddenError:
        logging.warning("Бот не может отправить сообщение - нет доступа")
    except Exception as e:
        logging.warning(f"Ошибка в help команде: {e}")

# --- Обработка рп-команд ---
@dp.message()
async def rp_action(message: Message):
    try:
        # Пропускаем служебные сообщения
        if message.left_chat_member or message.new_chat_members:
            return
            
        original_text = message.text.strip() if message.text else ""
        text = original_text.lower()
        
        # Нормализуем текст (заменяем ё на е)
        normalized_text = normalize_text(text)
        
        # Простая и надежная проверка: ищем команду в тексте
        matched_command = None
        for command in all_commands.keys():
            # Нормализуем команду для сравнения
            normalized_command = normalize_text(command.lower())
            
            # Проверяем, содержится ли команда в тексте как отдельное слово
            if normalized_command in normalized_text:
                # Убедимся, что это не часть другого слова
                words = normalized_text.split()
                if normalized_command in words:
                    matched_command = command
                    break
                # Также проверяем границы текста
                elif (normalized_text.startswith(normalized_command + " ") or 
                      normalized_text.endswith(" " + normalized_command) or 
                      normalized_text == normalized_command):
                    matched_command = command
                    break

        if matched_command:
            emoji = all_commands[matched_command]
            if message.reply_to_message:  # если команда в ответ на сообщение
                target = message.reply_to_message.from_user
                await message.reply(
                    f"{emoji} Пользователь @{message.from_user.username or message.from_user.first_name} {matched_command} @{target.username or target.first_name} {emoji}")
            else:
                # если команда с упоминанием
                entities = message.entities or []
                target = None
                for e in entities:
                    if e.type == 'mention' or e.type == 'text_mention':
                        if hasattr(e, 'user'):
                            target = e.user
                        break
                
                if target:
                    await message.reply(
                        f"{emoji} Пользователь @{message.from_user.username or message.from_user.first_name} {matched_command} @{target.username or target.first_name} {emoji}")
                else:
                    await message.reply(
                        f"{emoji} Чтобы использовать команду, ответь на сообщение пользователя или упомяни его через @ {emoji}")

    except TelegramForbiddenError:
        logging.warning("Бот не может отправить сообщение - нет доступа к чату")
    except Exception as e:
        logging.warning(f"Ошибка в обработке команды: {e}")

async def main():
    logging.info("Бот запущен на Render!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка запуска бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())

