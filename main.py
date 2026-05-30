import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from effects import process_video
import os

TOKEN = "8854820353:AAHAvD18ooi032u58LvPnwT2bQLPy4o5VU4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً يا دراكون! أرسل لي فيديو وسأقوم بتصميمه لك.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_file = await update.message.video.get_file()
    await video_file.download_to_drive("input.mp4")
    
    keyboard = [
        [InlineKeyboardButton("أبيض وأسود", callback_data='bw')],
        [InlineKeyboardButton("تصميم بطيء", callback_data='slow')],
        [InlineKeyboardButton("تصميم معكوس", callback_data='reverse')]
    ]
    await update.message.reply_text("تم استلام الفيديو، اختر التصميم:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(text="جاري التصميم... انتظر لحظة.")
    
    process_video("input.mp4", "output.mp4", query.data)
    
    await query.message.reply_video(video=open("output.mp4", 'rb'))
    os.remove("input.mp4")
    os.remove("output.mp4")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(CallbackQueryHandler(button_click))
    print("--- البوت يعمل يا دراكون ---")
    app.run_polling()

