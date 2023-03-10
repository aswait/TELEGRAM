from loader import bot
from utils.logging import logger
from telebot.types import Message, CallbackQuery
from states.low_high_best import LowHighBest
from keyboards.inline.city_founding import city_markup
from keyboards.inline.hotels_count import hotels_count
from keyboards.inline.choice import choice
from keyboards.inline.photos_count import photos_count
from utils.my_style_calendar import MyStyleCalendar, LSTEP
from datetime import date, datetime, timedelta
from api.hotel_info import hotel_info
from handlers.custom_handlers.help import help_message
from states.start import Start
from api.hotel_founding import hotel_founding
from utils.info_message import info_message
from database.create_table import db_command


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"])
def low_high_best(message: Message) -> None:
    logger.info(f'user_name: {message.from_user.username} | user_id: {message.from_user.id} | command: {message.text}')
    bot.set_state(message.from_user.id, LowHighBest.start, message.chat.id)
    bot_message = bot.send_message(message.chat.id,
                                   "В каком городе ищем?".format(message.from_user.first_name))

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['message_id'] = bot_message.id
        data['command'] = message.text


@bot.message_handler(state=LowHighBest.start)
@logger.catch
def city(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.edit_message_text(f'💬 Введенные данные: {message.text}',
                              message_id=data['message_id'],
                              chat_id=message.chat.id)

        bot.delete_message(message.chat.id, message.message_id)
        bot_message = bot.send_message(message.from_user.id, '📌 Уточните пожалуйста:',
                                       reply_markup=city_markup(message.text))
        data['error'] = False
        data['second_message_id'] = bot_message.id


@bot.callback_query_handler(func=lambda call: 'city' in call.data)
@logger.catch
def callback_city(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['location_id'] = call.data.split()[1]
        data['search_info'] = f'📍 Выбранный город: {call.data.split()[2]}'

        bot.edit_message_text(data['search_info'],
                              message_id=data['message_id'],
                              chat_id=call.message.chat.id)

        if data['command'] == '/bestdeal':

            bot.edit_message_text(f'💲 Введите минимальную цену (в $ USD):',
                                  message_id=data['second_message_id'],
                                  chat_id=call.message.chat.id)
            bot.set_state(call.from_user.id, LowHighBest.min_price, call.message.chat.id)

        else:
            bot.edit_message_text(f'🧳 Сколько отелей будем смотреть?',
                                  message_id=data['second_message_id'],
                                  chat_id=call.message.chat.id,
                                  reply_markup=hotels_count())


@bot.callback_query_handler(func=lambda call: 'count' in call.data)
@logger.catch
def callback_hotel_count(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['hotels_count'] = int(call.data.split()[1])
        data['search_info'] = f"{data['search_info']}\n" \
                              f"🔎 Количество отелей: {data['hotels_count']}"

        bot.edit_message_text(data['search_info'],
                              message_id=data['message_id'],
                              chat_id=call.message.chat.id)

        calendar, step = MyStyleCalendar(locale='ru', min_date=date.today()).build()
        bot.edit_message_text(f"🗓 Планируемая дата заезда: \n"
                              f"📌 Выберите {LSTEP[step]}",
                              message_id=data['second_message_id'],
                              chat_id=call.message.chat.id,
                              reply_markup=calendar)


@bot.callback_query_handler(func=MyStyleCalendar.func())
@logger.catch
def cal(call: CallbackQuery) -> None:
    result, key, step = MyStyleCalendar(locale='ru', min_date=date.today()).process(call.data)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        if not result and key:
            bot.edit_message_text(text=f"🗓 Планируемая дата заезда: \n"
                                       f"📌 Выберите {LSTEP[step]}",
                                  chat_id=call.message.chat.id,
                                  message_id=data['second_message_id'],
                                  reply_markup=key)
        elif result:
            data['check_in'] = result.strftime('%Y-%m-%d')
            data['search_info'] = f"{data['search_info']}\n" \
                                  f"➡ Дата заезда: {result}"

            bot.edit_message_text(data['search_info'],
                                  call.message.chat.id,
                                  data['message_id'])

            bot.edit_message_text(text=f"📅 Планируемое кол-во дней для бронирования?",
                                  chat_id=call.message.chat.id,
                                  message_id=data['second_message_id'])

            bot.set_state(call.from_user.id, LowHighBest.check_out, call.message.chat.id)


@bot.message_handler(state=LowHighBest.check_out)
@logger.catch
def check_out(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            if not message.text.isdigit():
                raise ValueError
            elif 1 > int(message.text):
                raise ValueError
            else:

                data['period'] = message.text
                check_out_date = datetime.strptime(data['check_in'], '%Y-%m-%d') + timedelta(days=int(message.text))
                data['check_out'] = check_out_date.strftime('%Y-%m-%d')

                req_filter = dict()
                req_filter['availableFilter'] = 'SHOW_AVAILABLE_ONLY'
                if data['command'] == '/lowprice':
                    sort = 'PRICE_LOW_TO_HIGH'
                elif data['command'] == '/highprice':
                    sort = 'PRICE_HIGH_TO_LOW'
                elif data['command'] == '/bestdeal':
                    sort = 'DISTANCE'
                    req_filter['price'] = {'max': data['max_price'], 'min': data['min_price']}

                data['hotel_id_list'] = hotel_founding(data['location_id'],
                                                       datetime.strptime(data['check_in'], '%Y-%m-%d'),
                                                       datetime.strptime(data['check_out'], '%Y-%m-%d'),
                                                       data['hotels_count'],
                                                       sort=sort,
                                                       req_filter=req_filter)

                data['search_info'] = f"{data['search_info']}\n" \
                                      f"⬅ Дата выезда: {data['check_out']}"
                if data['error']:
                    bot.delete_message(chat_id=message.chat.id,
                                       message_id=data['error'].split()[1])

                bot.delete_message(chat_id=message.chat.id,
                                   message_id=message.id)

                bot.edit_message_text(data['search_info'],
                                      message.chat.id,
                                      data['message_id'])

                bot.edit_message_text(text=f"📷 Будем загружать и выводить фотографии отеля?",
                                      chat_id=message.chat.id,
                                      message_id=data['second_message_id'],
                                      reply_markup=choice())
                data['error'] = False

        except ValueError:
            if data['error']:
                bot.delete_message(chat_id=message.chat.id,
                                   message_id=data['error'].split()[1])

            error = bot.send_message(chat_id=message.chat.id,
                                     text='❗ Ошибка, повторите ввод. Кол-во дней?')
            data['error'] = f"error {error.id}"

            bot.delete_message(chat_id=message.chat.id,
                               message_id=message.id)


@bot.callback_query_handler(func=lambda call: 'No' in call.data)
@logger.catch
def without_photo(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        result = hotel_info(data['hotel_id_list'])

        edit(call.message.chat.id,
             data['message_id'],
             data['second_message_id'])

        for hotel in result:
            bot.send_message(chat_id=call.message.chat.id,
                             text=info_message(hotel=hotel,
                                               period=data['period']))

        db_command(result, call.from_user.id, data['command'])
        bot.set_state(call.from_user.id, Start.start)
        bot.send_message(chat_id=call.message.chat.id, text=help_message())


@bot.callback_query_handler(func=lambda call: 'Yes' in call.data)
@logger.catch
def with_photo(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        bot.edit_message_text(text=f"🖼 Сколько фото будем выводить?",
                              chat_id=call.message.chat.id,
                              message_id=data['second_message_id'],
                              reply_markup=photos_count())


@bot.callback_query_handler(func=lambda call: 'photo' in call.data)
@logger.catch
def photos(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        result = hotel_info(data['hotel_id_list'], int(call.data.split()[1]))

        edit(call.message.chat.id,
             data['message_id'],
             data['second_message_id'])

        for hotel in result:
            bot.send_message(chat_id=call.message.chat.id,
                             text=info_message(hotel=hotel,
                                               period=data['period']))
            bot.send_media_group(call.message.chat.id, hotel['images'])

        db_command(result, call.from_user.id, data['command'])
        bot.set_state(call.from_user.id, Start.start)
        bot.send_message(chat_id=call.message.chat.id, text=help_message())


@bot.message_handler(state=LowHighBest.min_price)
@logger.catch
def max_price(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            if not message.text.isdigit():
                raise ValueError
            elif 1 > int(message.text):
                raise ValueError
            else:
                data['min_price'] = int(message.text)

                if data['error']:
                    bot.delete_message(chat_id=message.chat.id,
                                       message_id=data['error'].split()[1])

                data['search_info'] = f"{data['search_info']}\n" \
                                      f"💰 Минимальная цена: {data['min_price']}"

                bot.delete_message(chat_id=message.chat.id,
                                   message_id=message.id)

                bot.edit_message_text(data['search_info'],
                                      message.chat.id,
                                      data['message_id'])

                bot.edit_message_text(text=f"💲 Введите максимальную цену (в $ USD):",
                                      chat_id=message.chat.id,
                                      message_id=data['second_message_id'])
                data['error'] = False
                bot.set_state(message.from_user.id, LowHighBest.max_price, message.chat.id)

        except ValueError:
            if data['error']:
                bot.delete_message(chat_id=message.chat.id,
                                   message_id=data['error'].split()[1])

            error = bot.send_message(chat_id=message.chat.id,
                                     text='❗ Ошибка, повторите ввод. Кол-во дней?')
            data['error'] = f"error {error.id}"

            bot.delete_message(chat_id=message.chat.id,
                               message_id=message.id)


@bot.message_handler(state=LowHighBest.max_price)
@logger.catch
def max_price(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            if not message.text.isdigit():
                raise ValueError
            elif 1 > int(message.text):
                raise ValueError
            else:
                data['max_price'] = int(message.text)

                if data['error']:
                    bot.delete_message(chat_id=message.chat.id,
                                       message_id=data['error'].split()[1])

                data['search_info'] = f"{data['search_info']}\n" \
                                      f"💰 Максимальная цена: {data['max_price']}"

                bot.delete_message(chat_id=message.chat.id,
                                   message_id=message.id)

                bot.edit_message_text(data['search_info'],
                                      message.chat.id,
                                      data['message_id'])

                bot.edit_message_text(f'🧳 Сколько отелей будем смотреть?',
                                      message_id=data['second_message_id'],
                                      chat_id=message.chat.id,
                                      reply_markup=hotels_count())

                data['error'] = False

        except ValueError:
            if data['error']:
                bot.delete_message(chat_id=message.chat.id,
                                   message_id=data['error'].split()[1])

            error = bot.send_message(chat_id=message.chat.id,
                                     text='❗ Ошибка, повторите ввод. Кол-во дней?')
            data['error'] = f"error {error.id}"

            bot.delete_message(chat_id=message.chat.id,
                               message_id=message.id)


def edit(chat_id, first_id, second_id):
    bot.edit_message_text('ℹ Информация об отелях:',
                          chat_id,
                          first_id)

    bot.delete_message(chat_id,
                       second_id)
