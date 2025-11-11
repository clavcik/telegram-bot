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

# --- Список всех команд с эмодзи и прошедшим временем ---
all_commands = {
    "обнять": {"emoji": "🤗", "past": "обнял(а)"},
    "поцеловать": {"emoji": "💋", "past": "поцеловал(а)"},
    "дать пять": {"emoji": "🖐️", "past": "дал(а) пять"},
    "испугать": {"emoji": "😱", "past": "испугал(а)"},
    "извиниться": {"emoji": "🙏", "past": "извинился(лась)"},
    "куснуть": {"emoji": "🦷", "past": "куснул(а)"},
    "пнуть": {"emoji": "👟", "past": "пнул(а)"},
    "ударить": {"emoji": "🥊", "past": "ударил(а)"},
    "похвалить": {"emoji": "👏", "past": "похвалил(а)"},
    "погладить": {"emoji": "🫶", "past": "погладил(а)"},
    "поздравить": {"emoji": "🎉", "past": "поздравил(а)"},
    "пожать руку": {"emoji": "🤝", "past": "пожал(а) руку"},
    "шлёпнуть": {"emoji": "🍑", "past": "шлёпнул(а)"},
    "расстрелять": {"emoji": "🔫", "past": "расстрелял(а)"},
    "сжечь": {"emoji": "🔥", "past": "сжёг(сожгла)"},
    "пригласить на чаёк": {"emoji": "🍵", "past": "пригласил(а) на чаёк"},
    "понюхать": {"emoji": "👃", "past": "понюхал(а)"},
    "покормить": {"emoji": "🍽️", "past": "покормил(а)"},
    "потрогать": {"emoji": "✋", "past": "потрогал(а)"},
    "ущипнуть": {"emoji": "🤏", "past": "ущипнул(а)"},
    "связать": {"emoji": "🪢", "past": "связал(а)"},
    "повесить": {"emoji": "🪤", "past": "повесил(а)"},
    "уничтожить": {"emoji": "💣", "past": "уничтожил(а)"},
    "взорвать": {"emoji": "💥", "past": "взорвал(а)"},
    "щекотать": {"emoji": "😆", "past": "пощекотал(а)"},
    "арестовать": {"emoji": "👮", "past": "арестовал(а)"},
    "рассмешить": {"emoji": "😂", "past": "рассмешил(а)"},
    "ушатать": {"emoji": "🧱", "past": "ушатал(а)"},
    "порвать": {"emoji": "🧻", "past": "порвал(а)"},
    "выпороть": {"emoji": "🩸", "past": "выпорол(а)"},
    "сделать большой подарок": {"emoji": "🎁", "past": "сделал(а) большой подарок"},
    "устроить сюрприз": {"emoji": "🎊", "past": "устроил(а) сюрприз"},
    "подарить шоколадку": {"emoji": "🍫", "past": "подарил(а) шоколадку"},
    "поговорить по душам": {"emoji": "💞", "past": "поговорил(а) по душам"},
    "сходить в кино": {"emoji": "🎬", "past": "сходил(а) в кино"},
    "пригласить погулять": {"emoji": "🌆", "past": "пригласил(а) погулять"},
    "сделать комплимент": {"emoji": "🌹", "past": "сделал(а) комплимент"}
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
    text += "1. Ответь на сообщение пользователя с командой\n"
    text += "2. Употреби команду с @юзернейм\n"
    text += "Пример: <code>обнять @username</code>\n\n"
    text += "✨ Бот не реагирует на команды с обычными именами!"
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
        
        # Ищем команду в тексте (сначала без нормализации)
        matched_command = None
        
        for command in all_commands.keys():
            # Сначала проверяем оригинальную команду (с ё)
            if command in text:
                # Убедимся, что это не часть другого слова
                words = text.split()
                if command in words:
                    matched_command = command
                    break
                elif (text.startswith(command + " ") or 
                      text.endswith(" " + command) or 
                      text == command):
                    matched_command = command
                    break
        
        # Если не нашли с ё, пробуем с нормализацией
        if not matched_command:
            normalized_text = normalize_text(text)
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
            emoji = all_commands[matched_command]["emoji"]
            past_tense = all_commands[matched_command]["past"]
            
            # 1. Проверяем ответ на сообщение (приоритет)
            if message.reply_to_message:
                target = message.reply_to_message.from_user
                await message.reply(
                    f"{emoji} @{message.from_user.username or message.from_user.first_name} {past_tense} @{target.username or target.first_name} {emoji}")
                return
            
            # 2. Проверяем упоминания в тексте (@юзернейм)
            elif message.entities:
                has_mention = False
                for entity in message.entities:
                    # Обработка упоминаний через @username
                    if entity.type == "mention":
                        mention_text = original_text[entity.offset:entity.offset + entity.length]
                        if mention_text.startswith('@'):
                            has_mention = True
                            await message.reply(
                                f"{emoji} @{message.from_user.username or message.from_user.first_name} {past_tense} {mention_text} {emoji}")
                            return
                    
                    # Обработка текстовых упоминаний (когда Telegram предоставляет User объект)
                    elif entity.type == "text_mention":
                        if hasattr(entity, 'user') and entity.user:
                            has_mention = True
                            target = entity.user
                            await message.reply(
                                f"{emoji} @{message.from_user.username or message.from_user.first_name} {past_tense} @{target.username or target.first_name} {emoji}")
                            return
                
                # Если есть команда, но нет упоминаний - игнорируем
                if not has_mention:
                    return
            
            # 3. Если нет ответа и нет упоминаний - игнорируем команду
            return

    except Exception as e:
        logging.warning(f"Ошибка: {e}")

async def main():
    logging.info("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
