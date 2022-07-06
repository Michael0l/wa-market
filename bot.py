from telebot import types
from telebot.types import LabeledPrice
from bot_tools import board, products, categories
from create import bot
import config
from pprint import pprint



@bot.message_handler(commands=['start'])
def cmd_start(message: types.Message):
    markup = types.InlineKeyboardMarkup(keyboard=[[types.InlineKeyboardButton(text="Перейти к каталогу 🚀", web_app=types.WebAppInfo(url=config.url_web_market),)]])
    bot.send_message(message.chat.id, 'Приветствую тебя! Посети наш сайт!', reply_markup=markup)



@bot.message_handler(commands=['form'])
def cmd_form(message: types.Message):
    markup = types.InlineKeyboardMarkup(
        keyboard=[[types.InlineKeyboardButton(text="Заполнить форму",web_app=types.WebAppInfo(url=config.url_web_form),)]])
    bot.send_message(message.from_user.id, "<b>Привет!</b>\nОтправь мне сообщение с контактами!", reply_markup=markup)



# @bot.message_handler(func=lambda message: message.via_bot)
# def ordered(message: types.Message):
#     products = message.text.split('\n')[2:-2]
#     print(products)
#     lst = []
#     for el in products:
#         name, amount = el.split(' - ')[0]
#         price = ''.join(el.split(' - ')[1].split()[0:2])
#         print(price)
#         lst.append(LabeledPrice(label=name, amount=int(price)*100))

#     user_id = message.chat.id
#     bot.send_invoice(user_id, title='Оплата заказа',
#                         description='💸 Сумма платежа в 10 раз меньше, так как в тестовом режиме есть ограчичение на максимальную сумму',
#                         invoice_payload=f'deposit',
#                         provider_token='381764678:TEST:38655',
#                         currency='RUB',
#                         start_parameter='test',
#                         prices=lst)



@bot.pre_checkout_query_handler(func=lambda pre_checkout_query: True)
def query_handler(pre_checkout_query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



@bot.message_handler(content_types=['successful_payment'])
def query_handler(message):
    user_id = message.from_user.id
    msg_id_answer = message.successful_payment.invoice_payload.split('_')[1]
    adres = message.successful_payment.order_info
    pprint(vars(adres.shipping_address))
    bot.send_message(config.notification_chat_id, f'Успешная оплата!\n\nТелефон: +{adres.phone_number}\nАдрес: {adres.shipping_address.country_code} {adres.shipping_address.state} {adres.shipping_address.city} {adres.shipping_address.street_line1}\nИндекс: {adres.shipping_address.post_code}', reply_to_message_id=msg_id_answer)
    bot.send_message(user_id, 'Успешная оплата!')




@bot.message_handler(commands=['admin'])
def cmd_admin(message):
    bot.send_message(message.from_user.id, "👨‍💻 Админ панель", reply_markup=board.admin_panel())



@bot.callback_query_handler(func=lambda call: True)
def callback_func(call):
    calldata = call.data
    if calldata == 'product':
        products.send_list_products(call.message)
    elif calldata == 'add_product':
        products.add_products(call.message)
    elif calldata == 'edit_product':
        products.edit_product_id(call.message)
    elif calldata.startswith('edit_product_'):
        products.edit_product(call)

    elif calldata == 'categories':
        categories.send_list_categories(call.message)
    elif calldata == 'add_category':
        categories.add_category(call.message)
    elif calldata == 'edit_category':
        categories.edit_category_id(call.message)
    elif calldata == 'del_category':
        categories.del_category_id(call.message)



if __name__ == "__main__":
    bot.infinity_polling()