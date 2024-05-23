from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes, 
    CallbackQueryHandler, 
    JobQueue)
from datetime import datetime, time, timedelta
import pytz

async def calculate_life_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("success user pressed to calculate")
    query = update.callback_query
    await query.answer()
    birth_date = datetime(2000, 1, 1, tzinfo=pytz.timezone('Europe/Berlin'))
    today = datetime.now(pytz.timezone('Europe/Berlin'))

    # Calculate days lived
    days_lived = (today - birth_date).days
    
    # Constants
    estimated_age = 66
    month_to_day = 30.4167

    # Calculate months, weeks, and years lived
    months_lived = days_lived / month_to_day
    weeks_lived = days_lived / 7
    years_lived = days_lived / 365

    # Calculate days, weeks, months, and years left
    days_left = estimated_age * 365 - days_lived
    weeks_left = estimated_age * 52 - weeks_lived
    months_left = estimated_age * 12 - months_lived
    years_left = estimated_age - years_lived

    stats_message = (
        f"Days lived: {days_lived:.0f}\n"
        #f"Months lived: {months_lived:.0f}\n"
        f"Weeks lived: {weeks_lived:.0f}\n"
        #f"Years lived: {years_lived:.1f}\n\n"
        f"Days left: {days_left:.0f}\n"
        f"Weeks left: {weeks_left:.0f}\n"
        #f"Months left: {months_left:.0f}\n"
        #f"Years left: {years_left:.0f}\n"
    )

    await query.edit_message_text(text=stats_message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Calculate Life Stats", callback_data='calculate_life_stats')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('MENU:', reply_markup=reply_markup)
    print("test starting")


app = ApplicationBuilder().token("TOKEN!!!!").build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(calculate_life_stats, pattern='calculate_life_stats'))

app.run_polling()