import json
import os
import subprocess
from pathlib import Path
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from vosk import Model, KaldiRecognizer

router = Router()
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)


@router.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Это Бот для конвертации голосового/аудио сообщения в текст. "
        "Перешли боту голосовое сообщение,а он отправит тебе его текст :)"
    )


@router.message()
async def voice_message_handler(message: types.Message):
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_on_disk = Path("voice_messages", f"{file_id}.ogg")
        await bot.download_file(file_path, destination=file_on_disk)
        text = voice_to_text(file_on_disk)
        if len(text) > 4096:
            for x in range(0, len(text), 4096):
                await message.bot.send_message(message.chat.id, text[x:x + 4096])
        elif len(text) == 0:
            await message.reply("Слишком плохо слышно либо сообщение без речи!")
        else:
            await message.answer(text)
    elif message.content_type == types.ContentType.TEXT:
        await message.reply("Только голосовые сообщения!")
    else:
        await message.reply("Формат файла не поддерживается")
        return


def voice_to_text(file_on_disk):
    model = Model("model/vosk-model-small-ru-0.22")
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    ffmpeg_path = "model/vosk-model-small-ru-0.22/ffmpeg.exe"
    process = subprocess.Popen(
        [ffmpeg_path,
         "-loglevel", "quiet",
         "-i", file_on_disk,
         "-ar", "15000",
         "-ac", "1",
         "-f", "wav",
         "-"],
        stdout=subprocess.PIPE
    )
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            pass
    os.remove(file_on_disk)
    result_json = recognizer.FinalResult()
    result_dict = json.loads(result_json)
    return result_dict["text"]


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

