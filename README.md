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
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Settings**:
   Edit `config.py` with your settings:
   - `TOKEN`: Your Telegram bot token.
   - `ADMIN_ID`: Your Telegram user ID.
   - `HOST`: Host for the Flask app (default: `0.0.0.0` for external access).
   - `PORT`: Port for the Flask app (default: `10000`).
   - `DATABASE`: Path to the SQLite database (default: `events.db`).

## Usage

1. **Run the Application**:
   ```bash
   python app.py
   ```

2. **Interact with the Bot**:
   - Start the bot by sending `/start` in Telegram (admin only).
   - Add an event by sending a message in the format `HH:MM Event Name` (e.g., `13:30 Start of Broadcast`).
   - The bot will confirm if the event is added as the main or secondary event.

3. **View Events**:
   - Open a browser and navigate to `http://<HOST>:<PORT>/` to view the web interface.
   - The API endpoint `http://<HOST>:<PORT>/api/events` returns event data in JSON format.

## Project Structure
```
├── app.py              # Main application (Flask app and Telegram bot)
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web interface template
└── events.db           # SQLite database (created on first run)
```

## API Endpoints
- `GET /`: Renders the web interface (`index.html`).
- `GET /api/events`: Returns a JSON object with:
  - `mainEvent`: The main event (name and time) or a default if none exists.
  - `secondaryEvents`: A list of secondary events (name and time).

## Notes
- The bot uses the `aiogram` library for Telegram integration and `flask` for the web server.
- The SQLite database is initialized automatically on the first run.
- The bot runs in a separate thread to avoid blocking the Flask server.
- Ensure the `HOST` and `PORT` are accessible if deploying externally (e.g., configure firewall or port forwarding).

## Troubleshooting
- **Bot not responding**: Verify the `TOKEN` and `ADMIN_ID` in `config.py`. Ensure the bot is not blocked in Telegram.
- **Web interface not loading**: Check if the Flask server is running and the `HOST`/`PORT` are correct.
- **Database errors**: Ensure the directory for `events.db` is writable.

## Contributing
Feel free to submit issues or pull requests on [GitHub](https://github.com/eg-rek).

## Author
- **Eg_Rek**
- Telegram: [t.me/eg_rek](https://t.me/eg_rek)
- GitHub: [github.com/eg-rek](https://github.com/eg-rek)

## License
This project is licensed under the MIT License.
```
