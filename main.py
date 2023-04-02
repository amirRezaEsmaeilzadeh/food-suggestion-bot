import os
import telebot
import requests
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
isLoopStarted = False


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(chat_id=message.chat.id, text="HI!!"
                                                   "\nI'm your Food Suggestion Telegram bot."
                                                   "\nType in /im_hungry to get a random recipe")


@bot.message_handler(commands=["im_hungry"])
def handle_hunger(message):
    response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php").json()
    mealThumb = response["meals"][0]["strMealThumb"]
    mealName = response["meals"][0]["strMeal"]
    instructions = response['meals'][0]['strInstructions']
    bot.send_photo(message.chat.id, mealThumb)
    bot.send_message(message.chat.id, text=mealName)
    bot.send_message(message.chat.id, text=instructions)

    for index in range(1, 21):
        ingredients = response['meals'][0][f'strIngredient{index}']
        measures = response['meals'][0][f'strMeasure{index}']
        bot.send_message(message.chat.id, text=f"{measures} {ingredients}")    


bot.infinity_polling()
