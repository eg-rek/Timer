# -*- coding: utf-8 -*-
# @Time    : 2025/5/12 00:00
# @Author  : Eg_Rek
# @File    : app.py
# @Software: Visual Studio Code
# @Telegram: https://t.me/eg_rek
# @GitHub: https://github.com/eg-rek

import os
import asyncio
import sqlite3
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, ADMIN_ID, HOST, PORT, DATABASE

app = Flask(__name__)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS events
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     is_main INTEGER DEFAULT 0,
                     name TEXT,
                     time TEXT)''')

def add_event(name: str, time: str, is_main: bool = False):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        if is_main:
            cur.execute("UPDATE events SET is_main = 0 WHERE is_main = 1")
        cur.execute("INSERT INTO events (is_main, name, time) VALUES (?, ?, ?)",
                   (1 if is_main else 0, name, time))
        conn.commit()

@dp.message(Command("start"))
async def start(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("🚫 Доступ запрещен")
    
    await message.answer(
        "👋 Привет! Отправь время и название события в формате:\n"
        "<code>13:30 Начало трансляции</code>\n\n"
        "Первое событие станет главным."
    )

@dp.message(F.text)
async def add_event_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        time_str, *name = message.text.split()
        now = datetime.now()
        event_time = datetime.strptime(time_str, "%H:%M").time()
        full_datetime = datetime.combine(now.date(), event_time)
        event_name = " ".join(name)
        
        events = get_events()
        is_main = not events["main"]
        
        add_event(event_name, full_datetime.isoformat(), is_main)
        status = "главным" if is_main else "дополнительным"
        await message.answer(f"✅ Событие добавлено как {status}!")
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("❌ Неверный формат. Пример:\n<code>13:30 Начало трансляции</code>")

def get_events():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        main = cur.execute("SELECT name, time FROM events WHERE is_main = 1").fetchone()
        secondary = cur.execute("SELECT name, time FROM events WHERE is_main = 0 ORDER BY time").fetchall()
        
        return {
            "main": {"name": main["name"], "time": main["time"]} if main else None,
            "secondary": [{"name": e["name"], "time": e["time"]} for e in secondary]
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/events')
def api_events():
    events = get_events()
    return jsonify({
        "mainEvent": events["main"] or {"name": "Нет событий", "time": datetime.now().isoformat()},
        "secondaryEvents": events["secondary"]
    })

async def run_bot():
    try:
        await dp.start_polling(bot, parse_mode="HTML", handle_signals=False)
    except asyncio.CancelledError:
        pass

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == '__main__':
    init_db()
    
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    app.run(host=HOST, port=PORT, debug=False)