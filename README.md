# 📊 Stake Crash Bot – Telegram Alert System

This Python bot uses **Playwright (async)** to monitor real-time crash multipliers on [Stake Crash Game](https://stake.games/casino/games/crash), and sends **alerts via Telegram** when a pattern of low multipliers is detected.

---

## 🚀 Features

- ✅ Headless Playwright scraping
- 📈 Real-time crash value monitoring
- 🤖 Telegram bot integration
- ⚠️ Pattern-based alerting with suppression
- 🧠 Smart message cleanup and deduplication

---

## 🧰 Requirements

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

Install dependencies:

```bash
pip install playwright pyTelegramBotAPI
playwright install


Create a db.py file in the root directory with the following:

TOKEN = "your_telegram_bot_token"
USER_ID = your_telegram_user_id  # as integer
message = "🚨 Signal detected!"
count_falhas = 3  # Number of low values before alert
cout_vela = 2.00  # Threshold value (e.g., below 2x triggers count)


💬 Example Output

📌 Result: 1.74
📌 Result: 1.31
📌 Result: 1.98
⚠️ Alert! Only 1 more to reach the limit of 3..
🚨 Signal detected!
📈 1.52x 📉
Results: [1.74, 1.31, 1.98]
