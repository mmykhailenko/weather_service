FROM python:3

RUN mkdir -p /opt/telegram_bot
WORKDIR /opt/telegram_bot

ADD PoC_bot.py /opt/telegram_bot

RUN pip install pyTelegramBotAPI
RUN pip install requests
RUN pip install flask

CMD python PoC_bot.py