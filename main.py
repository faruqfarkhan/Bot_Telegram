from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, Defaults
import sql
import youtube_dl
import logging
import yt_dlp
import os


TOKEN : final = '7927428464:AAFOSNgSXGnyX8OikHBQcCPVL1uB-kYRc4Y'
BOT_USERNAME : final = '@ruquruqu_bot'



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# app.add_handler(CommandHandler('download_video',download_video))
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0]
    chat_id = update.message.chat_id

    # Periksa apakah pesan adalah tautan
    if not url.startswith("http"):
        await update.message.reply_text("Harap kirimkan tautan yang valid!")
        return

    await update.message.reply_text("Sedang memproses video, harap tunggu...")

    # Unduh video dengan yt_dlp
    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': f'downloaded_video{chat_id}.mp4',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file_path = f'downloaded_video{chat_id}.mp4'

        # Kirim video ke pengguna   
        try:
            with open(file_path, 'rb') as video:
                await context.bot.send_video(chat_id=chat_id, video=video, caption=f"Berikut videonya!, {chat_id}")
        finally:
            # File akan dihapus di blok finally
            if os.path.exists(file_path):
                os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan: {e}")

#command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Hello for chatting me')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
    start - untuk memulai bot 
    help - memanggil bantuan 
    add_task - tambahkan <deskripsi> untuk menambah tugas baru.
    list_tasks - untuk menampilkan semua daftar tugas. 
    pending_task - menampilkan pending task 
    show_task - <task_id> menampilkan 1 id 
    done - tambahkan <task_id> untuk menandai tugas sebagai selesai. 
    checkin - <id> untuk mencatat kehadiran. 
    checkout - <id> untuk mencatat waktu pulang.
    attendance - untuk melihat seluruh laporan absensi.

    ''')

# app.add_handler(CommandHandler('attendance',attendance))
async def attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = sql.list_sql()
    await update.message.reply_text(response, parse_mode="MarkdownV2")

# app.add_handler(CommandHandler('list_tasks',list_tasks))
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = sql.list_tasks_sql()
    await update.message.reply_text(response, parse_mode="MarkdownV2")


async def show_task(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    # Ambil teks setelah command
    text = context.args  # context.args adalah daftar dari argumen command

    if not text:  # Jika tidak ada argumen
        await update.message.reply_text('Masukan ID setelah perintah /show_task')
    else:
        try:
            task_id = text[0]  # Ambil argumen pertama sebagai ID
            # Panggil fungsi SQL dengan task_id
            response = sql.show_one_task_sql(task_id)
            await update.message.reply_text(response, parse_mode="MarkdownV2")
        except Exception as e:
            await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")

# app.add_handler(CommandHandler('add_task',add_task))
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    text = "".join(str(x) for x in context.args)  # context.args adalah daftar dari argumen command
    if not text:  # Jika tidak ada argumen
        await update.message.reply_text('Masukan Deskripsi setelah perintah /show_task')
    else:
        try:    
            print(text)  # Ambil argumen pertama sebagai ID
            # Panggil fungsi SQL dengan task_id
            response = sql.add_task_sql(text)
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")

# app.add_handler(CommandHandler('pending_task',pending_task))
async def pending_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = sql.pending_tasks_sql()
    await update.message.reply_text(response, parse_mode="MarkdownV2")
    
# app.add_handler(CommandHandler('done',done_task))
async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE): 

    text = context.args 
    if not text:  # Jika tidak ada argumen
        await update.message.reply_text('Masukan id task yang ingin di selesaikan')
    else:
        try:    
            print(text)  # Ambil argumen pertama sebagai ID
            # Panggil fungsi SQL dengan task_id
            response = sql.done_tasks_sql(text[0])
            await update.message.reply_text(response, parse_mode="MarkdownV2")
        except Exception as e:
            await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")
    
# app.add_handler(CommandHandler('checkin',checkin))
async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    text = context.args  # context.args adalah daftar dari argumen command
    if not text:  # Jika tidak ada argumen
        await update.message.reply_text('Masukan Deskripsi setelah perintah /checkin')
    else:
        try:    
            print(text[0])  # Ambil argumen pertama sebagai ID
            # Panggil fungsi SQL dengan task_id
            response = sql.checkin_sql(text[0])
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")

# app.add_handler(CommandHandler('checkout',checkout))
async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    text = context.args  # context.args adalah daftar dari argumen command
    if not text:  # Jika tidak ada argumen
        await update.message.reply_text('Masukan Deskripsi setelah perintah /checkout')
    else:
        try:    
            print(text[0])  # Ambil argumen pertama sebagai ID
            # Panggil fungsi SQL dengan task_id
            response = sql.checkout_sql(text[0])
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")

    


#Response
def handle_response(text: str) -> str:
    text_lower = text.lower()
    if 'hello' in text_lower:
        return 'hello there'
    elif 'how are you' in text_lower:
        return 'im fine, how about you'
    else:
        return 'saya tidak paham'
    

async def handle_massage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str = update.message.text

    print(f'user ({update.message.chat.id}) in ({message_type}) sending ({text})')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text : str = text.replace(BOT_USERNAME,'').strip()
            response : str = handle_response(text)
        else:
            return 'tes'
    else :
        response: str =handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} cause error {context.errorS}')

if __name__ == '__main__':
    print('start')
    app = Application.builder().token(TOKEN).read_timeout(120).write_timeout(120).build()

    #command
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('attendance',attendance))
    app.add_handler(CommandHandler('help',help))
    app.add_handler(CommandHandler('show_task',show_task))
    app.add_handler(CommandHandler('pending_task',pending_task))
    app.add_handler(CommandHandler('add_task',add_task))
    app.add_handler(CommandHandler('done',done_task))
    app.add_handler(CommandHandler('download_video',download_video))
    app.add_handler(CommandHandler('checkin',checkin))
    app.add_handler(CommandHandler('checkout',checkout))
    app.add_handler(CommandHandler('list_tasks',list_tasks))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_massage))

    #error
    app.add_error_handler(error)
    
    #check untuk update
    app.run_polling(poll_interval=2)



