FROM python:3.10-alpine

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]