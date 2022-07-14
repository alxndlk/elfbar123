from telebot import types
import telebot
import config
import time
import os
os.path.dirname()

bot = telebot.TeleBot(config.TOKEN)
# Заполнишь этот массив продуктами потом
products = [
    {
        "name": "Coconut melon",
        "emoji": "🥥🍈",
        "price": 1500,
        "photo": os.path.dirname("static/Coconut_melon.webp"),
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Banana milk",
        "emoji": "🍌🥛",
        "photo": os.path.dirname("static/Banana_milk.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Grape",
        "emoji": "🍇",
        "photo": os.path.dirname("static/grape.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Strawberry ice cream",
        "emoji": "🍓🍧",
        "photo": os.path.dirname("static/strawberry_ice.cream.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Strawberry banana",
        "emoji": "🍓🍌",
        "photo": os.path.dirname("static/Strawberry_banana.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Banana ice",
        "emoji": "🍌🧊",
        "photo": os.path.dirname("static/banana_ice.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Grape energy",
        "emoji": "🍇🧃",
        "photo": os.path.dirname("static/Grape_energy.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Watermelon",
        "emoji": "🍉",
        "photo": os.path.dirname("static/melon.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Mango",
        "emoji": "🥭",
        "photo": os.path.dirname("static/mango.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Mango peach watermelon",
        "emoji": "🥭🍑🍉",
        "photo": os.path.dirname("static/Mango_peach_watermelon.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Strawberry kiwi",
        "emoji": "🍓🥝",
        "photo": os.path.dirname("static/kiwi_strawberry.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Pink lemonade",
        "emoji": "🥤",
        "photo": os.path.dirname("static/pink_lemonade.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Blueberry",
        "emoji": "🫐",
        "photo": os.path.dirname("static/blueberry.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    },
    {
        "name": "Blue razz lemonade",
        "emoji": "💎🥛",
        "photo": os.path.dirname("static/blue_razz.webp"),
        "price": 1500,
        "nicotine": 5,
        "quantity": 1
    }
]

def get_menu_markup():
    # Ответ на Просмотреть товар кнопками
    markup = types.InlineKeyboardMarkup(row_width=1)

    for index, product in enumerate(products):
        product_name = f"{product['emoji']}{product['price']}|{product['name']}"
        button = types.InlineKeyboardButton(product_name, callback_data=f"product_{index}")
        markup.add(button)

    return markup

def edit_message(call, text, markup):
    if text:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text,
                              parse_mode='html')
    if markup:
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup)
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        types.KeyboardButton("⭐Просмотреть товар"),
        types.KeyboardButton("⚙Связаться со службой поддержки")
    )

    bot.send_message(message.chat.id,
                     "Здравствуйте, {0.first_name}!\nЯ - официальный бот канала <b>ELf Bar | Prague</b>.\n\nЧем могу Вам помочь?".format(
                         message.from_user, bot.get_me()
                     ),
                     parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call)

    if call.data == 'buy_product':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text='👨Александр', url='https://t.me/alxnlvk', callback_data='left'),
                   types.InlineKeyboardButton(text="👩Арина", url="https://t.me/arina13th", callback_data='middle'),
                   types.InlineKeyboardButton(text="👨Егор", url="https://t.me/egornegativ",callback_data='right'))
        edit_message(call=call, text="<b>Выберете человека у которого будете заказывать товар:</b>", markup=markup)

    elif 'product' in call.data:
        product_index = call.data.split('_')[1]

        product = products[int(product_index)]

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton('Выбрать', callback_data="buy_product"), types.InlineKeyboardButton("Назад", callback_data='main_menu'))

        sticker = open(product['photo'], 'rb')

        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_sticker(call.message.chat.id, sticker)
        bot.send_message(call.message.chat.id, f"Ваш выбор: <b>{product['emoji']}{product['price']}|{product['name']}.</b>\nКоличество никотина:<b> {product['nicotine']}% </b>", parse_mode='html', reply_markup=markup)

    elif call.data == "main_menu":
        menu_markup = get_menu_markup()
        edit_message(call=call, text="<b>Список доступных товаров:</b>", markup=menu_markup)

@bot.message_handler(content_types=['text'])
def quest_1(message):
    localtime = time.localtime(time.time())

    # Можешь использовать вместо if else такой формат
    # match message.text:
    #     case "⭐Просмотреть товар":
    #         bot.send_message(message.chat.id, "<b>Список доступных товаров:</b>", parse_mode='html',
    #                          reply_markup=menu_markup)

    if message.chat.type == 'private':
        # Просмотреть товар кнопка
        if message.text == '⭐Просмотреть товар':
            menu_markup = get_menu_markup()

            # Ответ на Просмотреть товар в строчке
            bot.send_message(message.chat.id, "<b>Список доступных товаров:</b>", parse_mode='html',
                             reply_markup=menu_markup)

        elif message.text == "⚙Связаться со службой поддержки":
            if localtime.tm_hour in [23, 0, 1, 2, 3, 4, 6, 7, 8]:
                bot.send_message(message.chat.id,
                                 "🔕На данный момент поддержка не сможет Вам ответить.\n\n🕘Пожалуйста, пользуйтесь службой поддержки <b>с 9:00 до 23:00</b>, сейчас: <b>" + str(
                                     localtime.tm_hour) + ":" + str(
                                     localtime.tm_min) + " по чешскому времени.</b>\n\nЗаранее спасибо😌.",
                                 parse_mode='html')

            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                people_sasha = types.InlineKeyboardButton(text='👨Александр', url='https://t.me/alxnlvk', callback_data='left')
                people_arina = types.InlineKeyboardButton(text="👩Арина", url="https://t.me/arina13th", callback_data='middle')
                people_danya = types.InlineKeyboardButton(text="👨Егор", url="https://t.me/egornegativ",
                                                   callback_data='right')
                markup.add(people_sasha, people_arina, people_danya)
                bot.send_message(message.chat.id,
                                 "👤Выберете человека, который поможет Вам.\nПри этом детально опишите свою проблему.",
                                 parse_mode='html', reply_markup=markup)


        else:
            bot.send_message(message.chat.id,
                             'Я не знаю как ответить на данный запрос 😔\n\n<b>Воспользуйтесь кнопками которые находятся ниже.</b>\n\n• Если бот завис либо же не отвечает на запросы - напишите команду: <b>/start</b>.\n\n\n⚠️Если бот вовсе никак не реагирует на Ваши запросы, пожалуйста, напишите в службу поддержки. Она в кротчайшие сроки свяжется с Вами.',
                             parse_mode='html')


# RUN
bot.polling(none_stop=True)
