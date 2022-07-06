import config
from telebot import types
from create import bot
from telebot.types import LabeledPrice



def wa_send_message(data, init_data):
    query_id = init_data['query_id']
    user_id = init_data['user']['id']
    result_text = '🛍 <b>Ваш заказ:</b>\n\n'
    order_text, total_cost = get_order_text(data)
    result_text += order_text + f'\n💸 Общая стоимость: <b>{total_cost} ₽</b>'
    result = types.InlineQueryResultArticle(
        id=query_id,
        title='Order',
        input_message_content=types.InputTextMessageContent(message_text=result_text, parse_mode='html'))
    msg = bot.send_message(config.notification_chat_id, f'Новая заявка! <a href="tg://user?id={user_id}">Клиент - {user_id}</a>\n' + order_text + f'\nОбщая стоимость: <b>{total_cost} ₽</b>')
    bot.answer_web_app_query(query_id, result)
    creat_order(data, user_id, msg)


def get_order_text(data):
    order_text = ''
    total_cost, count = 0, 1
    for el in data['msg']:
        name, price, amount = data['msg'][el]
        order_text += f'{count}. {name} - <b>{price}</b> х{amount}\n'
        total_cost += int(price) * amount
        count += 1
    return order_text, total_cost



    
def creat_order(data, user_id, msg):
    lst = []
    for el in data['msg']:
        name, price, amount = data['msg'][el]
        prices = int(price) * amount
        print(price)
        lst.append(LabeledPrice(label=name, amount=int(prices)*1))
    bot.send_invoice(user_id, title='Оплата заказа',
                        description='Оплатите заказ, чтобы получить товар',
                        invoice_payload=f'deposit_{msg.message_id}',
                        provider_token='381764678:TEST:38655',
                        currency='RUB',
                        start_parameter='test',
                        need_phone_number=True,
                        need_shipping_address=True,
                        prices=lst)

