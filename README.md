# Timer
ver 1.0
# Event Management Bot

This project is a Telegram bot integrated with a Flask web application to manage and display events. The bot allows an admin to add events via Telegram, which are stored in a SQLite database. The Flask app provides a web interface to view these events, with one main event and multiple secondary events.

## Features
- **Telegram Bot**: Admin can add events in the format `HH:MM Event Name` (e.g., `13:30 Start of Broadcast`).
- **Main Event**: The first event added is marked as the main event. Subsequent events are secondary unless the main event is replaced.
- **Web Interface**: Displays the main event and a list of secondary events via a Flask-powered API.
- **SQLite Database**: Stores event data persistently.
- **Access Control**: Only the admin (specified by `ADMIN_ID`) can interact with the bot.

## Prerequisites
- Python 3.8+
- Telegram account and bot token (obtained via [BotFather](https://t.me/BotFather))
- Admin Telegram ID (obtainable via [UserInfoBot](https://t.me/userinfobot))

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eg-rek/event-management-bot.git
   cd event-management-bot
