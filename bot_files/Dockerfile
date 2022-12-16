FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN python3 -m pip install -U discord.py

CMD ["ls"]
CMD ["pip list | grep discord.py"]

CMD ["python3.10", "bot_skript(Version).py"]