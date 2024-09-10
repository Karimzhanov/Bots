from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.core.wsgi import get_wsgi_application
import os, logging
from apps.telegram_bot.models import Email
from asgiref.sync import sync_to_async 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_bot_project.settings')
application = get_wsgi_application()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

PRIVATE_CHANNEL_LINK = "ссылка на канал "

async def start(update: Update, context):
    await update.message.reply_text('Привет! Отправьте мне вашу почту, и я проверю, есть ли она в базе.')

async def check_email(update: Update, context):
    user_email = update.message.text.strip()

    email_exists = await sync_to_async(Email.objects.filter(email=user_email).exists)()

    if email_exists:
        await update.message.reply_text(f"Ваша почта найдена в базе. Вот ссылка на частный канал: {PRIVATE_CHANNEL_LINK}")
    else:
        await update.message.reply_text("Вашей почты нет в базе.")

def main():
    application = Application.builder().token("token").build()

    # Регистрация обработчика команды /start
    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_email))

    application.run_polling()

if __name__ == '__main__':
    main()
