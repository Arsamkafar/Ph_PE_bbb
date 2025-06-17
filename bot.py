import os, re
from aiogram import Bot, Dispatcher, executor, types
from downloader import download_from_pornhub

API_TOKEN = os.getenv('7745614128:AAFc3A0Eell5yNbSO_T71oOdMIuff_JS9Os')
ALLOWED_USER_ID = int(os.getenv('970993631'))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

VALID_LINK_REGEX = re.compile(r'https?://(?:www\.)?(pornhub\.com|phncdn\.com)/.+')

@dp.message_handler(commands=['start'])
async def start_cmd(m: types.Message):
    if m.from_user.id != ALLOWED_USER_ID:
        return await m.reply("❌ دسترسی نداری.")
    await m.reply("👋 لینک ویدیوی Pornhub رو بفرست.")

@dp.message_handler()
async def handle_message(m: types.Message):
    if m.from_user.id != ALLOWED_USER_ID:
        return await m.reply("❌ اجازه ندارید.")
    url = m.text.strip()
    if not VALID_LINK_REGEX.match(url):
        return await m.reply("❌ لینک معتبر نیست!")
    temp = "/tmp/ph_video.mp4"
    await m.reply("📥 در حال دانلود...")
    try:
        download_from_pornhub(url, temp)
        await bot.send_video(chat_id=m.chat.id, video=open(temp, 'rb'))
        os.remove(temp)
        await m.reply("✅ ارسال شد و از سرور حذف شد.")
    except Exception as e:
        await m.reply(f"❌ خطا:\n`{e}`", parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
