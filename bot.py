import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Токен бота
token = "8321577382:AAF8sPv8N41WUk1Sa8ZMbPIn6sQznkGzk6Q"

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

def normalize_text(text):
    return text.replace('ё', 'е')

def format_commands_list():
    commands_list = list(all_commands.keys())
    middle = len(commands_list) // 2
    left_column = commands_list[:middle]
    right_column = commands_list[middle:]
    
    text = "🎮 <b>Доступные рп-команды:</b>\n\n"
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
    text += "\n\nℹ️ <i>Команды с буквой 'ё' работают и с 'е'</i>"
    return text

@dp.message(Command('help', prefix='!'))
async def help_command(message: Message):
    try:
        text = format_commands_list()
        await message.answer(text, parse_mode='HTML')
    except Exception as e:
        logging.warning(f"Ошибка: {e}")

@dp.message()
async def rp_action(message: Message):
    try:
        # Пропускаем служебные сообщения
        if message.left_chat_member or message.new_chat_members:
            return
            
        original_text = message.text.strip() if message.text else ""
        text = original_text.lower()
        normalized_text = normalize_text(text)
        
        # Ищем команду в тексте
        matched_command = None
        for command in all_commands.keys():
            normalized_command = normalize_text(command.lower())
            
            if normalized_command in normalized_text:
                words = normalized_text.split()
                if normalized_command in words:
                    matched_command = command
                    break
                elif (normalized_text.startswith(normalized_command + " ") or 
                      normalized_text.endswith(" " + normalized_command) or 
                      normalized_text == normalized_command):
                    matched_command = command
                    break

        if matched_command:
            emoji = all_commands[matched_command]
            
            # 1. Проверяем ответ на сообщение (приоритет)
            if message.reply_to_message:
                target = message.reply_to_message.from_user
                await message.reply(
                    f"{emoji} Пользователь @{message.from_user.username or message.from_user.first_name} {matched_command} @{target.username or target.first_name} {emoji}")
                return
            
            # 2. Проверяем упоминания в тексте
            elif message.entities:
                for entity in message.entities:
                    # Обработка упоминаний через @username
                    if entity.type == "mention":
                        mention_text = original_text[entity.offset:entity.offset + entity.length]
                        if mention_text.startswith('@'):
                            await message.reply(
                                f"{emoji} Пользователь @{message.from_user.username or message.from_user.first_name} {matched_command} {mention_text} {emoji}")
                            return
                    
                    # Обработка текстовых упоминаний (когда Telegram предоставляет User объект)
                    elif entity.type == "text_mention":
                        if hasattr(entity, 'user') and entity.user:
                            target = entity.user
                            await message.reply(
                                f"{emoji} Пользователь @{message.from_user.username or message.from_user.first_name} {matched_command} @{target.username or target.first_name} {emoji}")
                            return
            
            # 3. Если нет ответа и нет упоминаний
            await message.reply(
                f"{emoji} Чтобы использовать команду, ответь на сообщение пользователя или упомяни его через @ {emoji}")

    except Exception as e:
        logging.warning(f"Ошибка: {e}")

async def main():
    logging.info("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
