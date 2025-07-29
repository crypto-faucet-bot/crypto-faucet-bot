# Crypto Faucet Bot 🤖🪙

Телеграм-бот для отображения крипто-кранов, учёта статистики и рефералов.

## 📦 Установка

1. Склонируйте репозиторий или скачайте ZIP:
```
git clone https://github.com/yourusername/crypto-faucet-bot.git
cd crypto-faucet-bot
```

2. Установите зависимости:
```
pip install -r requirements.txt
```

3. Вставьте свой токен в `.env`:
```
BOT_TOKEN=ваш_токен_бота
```

4. Запустите бота:
```
python bot.py
```

## 🚀 Деплой на Render

- Зарегистрируйтесь на [render.com](https://render.com)
- Подключите GitHub
- Новый Web Service
- Укажите Build Command: `pip install -r requirements.txt`
- Start Command: `python bot.py`
- Добавьте переменную окружения: `BOT_TOKEN=...`

## 📊 Команды

- `/start` — старт с учётом рефералов
- `/faucets` — список кранов
- `/stats` — статистика и ваша реферальная ссылка

## 📁 Структура

- `bot.py` — запуск бота
- `handlers.py` — обработчики команд
- `database.py` — SQLite с рефералами
- `faucets.json` — список кранов