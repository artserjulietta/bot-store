from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from logic import *

TOKEN = '6077941896:AAGbReizYk_FxNsV40lrmF1n7lBsW548cz8'
bot = TeleBot(TOKEN)


def card_of_item(bot, message, row):
        
    info = f"""
Товар:   {row[1]}
Цвет:  {row[3]}
Цена:  {row[2]} рублей
"""
    try:
        with open(f'images/{row[4]}', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    finally:
        bot.send_message(message.chat.id, info, reply_markup=gen_markup(row[0]))

def gen_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Добавить в корзину", callback_data=f'buy_{id}'))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("buy"):
        id = call.data[call.data.find("_")+1:]
        user_id = call.from_user.id
        manager.add_item_to_cart(user_id, id)
        bot.send_message(call.message.chat.id, "Товар добавлен в корзину")
        # Задание №2: отправь сообщение в чат "Товар добавлен в корзину"

@bot.message_handler(commands=['show_cart'])
def show_cart(message):
    rows = manager.show_cart(message.from_user.id)
    for row in rows:
        name = manager.get_name_of_item(row[0])[0][0]
        count = row[1]
        bot.send_message(message.chat.id,f"{name} - {count} шт.")


@bot.message_handler(commands=['show_store'])
def show_store(message):
    # Задание №1: получи данные из бд
    res = manager.show_items()
    res = "\n".join([x[1] for x in res]) 
    bot.send_message(message.chat.id,res)

@bot.message_handler(commands=['clear_cart'])
def clear_cart(message):
    user_id = message.from_user.id
    manager.delete(user_id)
    bot.send_message(message.chat.id,"Корзина очищена")



if __name__ == '__main__':
    manager = StoreManager(DATABASE)
    bot.infinity_polling()