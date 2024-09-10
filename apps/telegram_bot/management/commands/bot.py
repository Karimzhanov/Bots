from django.core.management.base import BaseCommand
from apps.telegram_bot.views import main

class Command(BaseCommand):
    help = 'Bot' 

    def handle(self, *args, **kwargs):
        print("START TELEGRAM BOT")
        main()  # Just call the main function directly
