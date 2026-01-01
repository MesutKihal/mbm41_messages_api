from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from telegram import Bot
from telegram.constants import ParseMode
import asyncio
from .models import Sender, Message
from django.db.models import Q
from datetime import date
import os
from dotenv import load_dotenv


@api_view(['POST', 'GET'])
def send(request):
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    #Define bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    async def send_message(text, chat_id):
        async with bot:
            await bot.send_message(text=text, chat_id=chat_id, parse_mode=ParseMode.HTML)

    async def run_bot(messages, chat_id):
        message = "".join(messages)
        await send_message(message, chat_id)

    sender = Sender.objects.get(Q(full_name=request.data['FULL_NAME']) | Q(email=request.data['EMAIL']) | Q(phone_number=request.data['PHONE_NUMBER']))
    messages  = [
                "<b>Sender Information:</b>\n",
                f"Full Name: {request.data['FULL_NAME']}\n",
                f"Email: {request.data['EMAIL']}\n",
                f"Phone Number: {request.data['PHONE_NUMBER']}\n\n",
                f"{request.data['MESSAGE']}",
                ]

    if not sender:
        Sender.objects.create(full_name=request.data['FULL_NAME'], email=request.data['EMAIL'], phone_number=request.data['PHONE_NUMBER'])

    if messages:
        message = Message.objects.filter(sender=sender, date=date.today())
        if not message:
            sender = Sender.objects.get(Q(full_name=request.data['FULL_NAME']) | Q(email=request.data['EMAIL']) | Q(phone_number=request.data['PHONE_NUMBER']))
            Message.objects.create(sender=sender, content="".join(messages))
            asyncio.run(run_bot(messages, CHAT_ID))
            return Response({"response": "Message was sent successfully"})
        else:
            return Response({"response": "this sender already sent a message"})
