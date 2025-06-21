from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import pandas as pd

BOT_TOKEN = "7900927113:AAE7NgOnGpznkIvaJUCQSKZeH5J_ozE8uVM"
API_KEY = "7e20d4d7afde48dda95594e4cc112cb0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is online! Use /analyse eur/usd")

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a symbol. E.g. /analyse eur/usd")
        return

    symbol = context.args[0].upper()
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&apikey={API_KEY}&outputsize=30"

    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data["values"])
        df["close"] = df["close"].astype(float)
        latest_price = df["close"].iloc[0]
        await update.message.reply_text(f"📈 {symbol} Latest Price: {latest_price}")
    except:
        await update.message.reply_text("⚠️ Error fetching data.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analyse", analyse))
app.run_polling()
