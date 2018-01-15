# -*- coding: utf-8 -*-
from telebot import *
import const
import sqlite3
import random
import model
import re

token = "503235612:AAFD0eWpdRMk_tk0GXFO11jF47uKg-tJDqE"
bot = TeleBot(token)

sex_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
male_button = types.KeyboardButton(const.male)
female_button = types.KeyboardButton(const.female)
sex_keyboard.add(male_button, female_button)

rate_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
for i in range(1, 6):
    rate_keyboard.add(types.KeyboardButton(str(i)))


# Get gift from database
def get_gift_from_db(sex):
    connection = sqlite3.connect(const.DATABASE_NAME)
    cursor = connection.cursor()
    count_query = "SELECT count(*) FROM " + const.TABLE_NAME + " WHERE sex = " + str(int(sex))
    count = cursor.execute(count_query).fetchall().pop(0)[0]
    selected_id = random.randint(1, count)
    select_query = "SELECT * FROM " + const.TABLE_NAME + " WHERE id = " + str(selected_id)
    db_gift = cursor.execute(select_query).fetchall().pop(0)
    connection.close()
    return model.Gift(db_gift[0], db_gift[1], db_gift[2], db_gift[3], db_gift[4], db_gift[5], db_gift[6])


# /start command
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id, const.start_message)


# /help command
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, const.help_message)


# /gift command
@bot.message_handler(commands=['gift'])
def gift_cmd(message):
    msg = bot.send_message(message.chat.id, const.select_sex, reply_markup=sex_keyboard)
    bot.register_next_step_handler(msg, get_gift)


# /rate command
@bot.message_handler(commands=['rate'])
def gift_cmd(message):
    gift_id = str(message.text).replace("/rate ", "")
    connection = sqlite3.connect(const.DATABASE_NAME)
    cursor = connection.cursor()
    count = cursor.execute("SELECT count(*) FROM " + const.TABLE_NAME).fetchall().pop(0)[0]
    connection.close()
    if re.match("^[0-9]+$", gift_id):
        const.temp = int(gift_id)
        if count >= const.temp >= 1:
            msg = bot.send_message(message.chat.id, const.rate_help, reply_markup=rate_keyboard)
            bot.register_next_step_handler(msg, rate)
        else:
            bot.send_message(message.chat.id, const.rate_not_correct_id)
    else:
        bot.send_message(message.chat.id, const.rate_not_correct_id)


# rate for gift function
def rate(message):
    bot.send_message(message.chat.id, const.wait, reply_markup=types.ReplyKeyboardRemove(rate_keyboard))
    connection = sqlite3.connect(const.DATABASE_NAME)
    cursor = connection.cursor()

    gift = cursor.execute(
        "SELECT mark, mark_count FROM " + const.TABLE_NAME + " WHERE id = " + str(const.temp)).fetchall().pop(0)
    old_mark = gift[0]
    new_mark_count = gift[1] + 1
    new_mark = (old_mark + float(message.text)) / new_mark_count
    cursor.execute("UPDATE " + const.TABLE_NAME + " SET mark = " + str(new_mark) + ", mark_count = " + str(
        new_mark_count) + " WHERE id = " + str(const.temp))
    connection.commit()
    bot.send_message(message.chat.id, const.rate_thanks)
    connection.close()


# get gift function
def get_gift(message):
    bot.send_message(message.chat.id, const.wait, reply_markup=types.ReplyKeyboardRemove(sex_keyboard))
    sex = True if message.text == const.male else False
    gift = get_gift_from_db(sex)
    msg = const.result_id + str(gift.gift_id) + "\n" + \
          const.result_name + gift.name + "\n" + \
          const.result_description + gift.description + "\n" + \
          const.result_mark + str(gift.mark) + "\n" + \
          const.result_mark_count + str(gift.mark_count) + "\n" + const.result_msg
    inline_keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Купить подарок", url=gift.link)
    inline_keyboard.add(button)
    bot.send_message(message.chat.id, msg, reply_markup=inline_keyboard)


# get undetected input
@bot.message_handler(content_types=["text"])
def undetected_input(message):
    bot.send_message(message.chat.id, const.error_message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
