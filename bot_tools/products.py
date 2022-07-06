from telebot import types
from database import db_file
from bot_tools import board
from create import bot
import config



def get_categoty_dct():
    categories = db_file.Categories.query.all()
    categories_dct = {el.categor_id:el.name for el in categories}
    return categories_dct

def send_list_products(message):
    user_id = message.chat.id
    products = db_file.Products.query.all()
    if products:
        categories_dct = get_categoty_dct()
        msg = ''
        for el in products:
            msg += f'{el.prod_id}. {el.name} - {el.price} ₽ - {categories_dct[el.category]}\n{el.description}\n\n'
    else:
        msg = 'Нет товаров'
    bot.send_message(user_id, msg, reply_markup=board.products_panel())



# ====================== ADD PRODUCT ====================== 

def add_products(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, 'Введите название товара')
    bot.register_next_step_handler(msg, get_name_product)



def get_name_product(message):
    user_id = message.chat.id
    dct = {}
    dct['name'] = message.text
    msg = bot.send_message(user_id, 'Введите описание')
    bot.register_next_step_handler(msg, get_description_product, dct)



def get_description_product(message, dct):
    user_id = message.chat.id
    dct['description'] = message.text
    msg = bot.send_message(user_id, 'Введите стоимость')
    bot.register_next_step_handler(msg, get_price_product, dct)



def get_price_product(message, dct):
    user_id = message.chat.id
    dct['price'] = message.text
    msg = bot.send_message(user_id, 'Отправьте фото товара')
    bot.register_next_step_handler(msg, get_photo_product, dct)



def get_photo_product(message, dct):
    user_id = message.chat.id
    dct['photo'] = message.photo[-1].file_id
    save_photo(message)
    msg = get_categories('Введите номер категории\n\n')
    msg = bot.send_message(user_id, msg)
    bot.register_next_step_handler(msg, get_category_product, dct)



def get_category_product(message, dct):
    user_id = message.chat.id
    dct['category'] = message.text
    db_file.add_product(dct)
    markup = types.InlineKeyboardMarkup(keyboard=[[types.InlineKeyboardButton(text="Перейти к каталогу 🚀", web_app=types.WebAppInfo(url=config.url_web_market),)]])
    bot.send_message(user_id, f'Товар добавлен на сайт!', reply_markup=markup)



# ====================== EDIT PRODUCT ====================== 

def save_photo(message):
    photo = message.photo[-1].file_id
    file_photo = bot.get_file(photo)
    dwl_photo = bot.download_file(file_photo.file_path)
    with open(f'web_app/static/products_photo/{photo}{".jpg"}', 'wb') as new_photo:
        new_photo.write(dwl_photo)


def get_categories(msg):
    categories = db_file.Categories.query.all()
    for el in categories:
        msg += f'{el.categor_id}. {el.name}\n'
    return msg



def edit_product_id(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, 'Введите id товара')
    bot.register_next_step_handler(msg, get_id_product)



def get_id_product(message):
    user_id = message.chat.id
    prod_id = message.text
    categories_dct = get_categoty_dct()
    product = db_file.Products.query.filter_by(prod_id=prod_id).first()
    msg = f'ID: {product.prod_id}\nНазвание: {product.name}\nЦена: {product.price} ₽\nКатегория: {categories_dct[product.category]}\nОписание:\n{product.description}'
    bot.send_photo(user_id, product.photo, msg, reply_markup=board.edit_product_inline(product.prod_id))


def edit_product(call):
    user_id = call.message.chat.id
    action, prod_id = call.data.split('_')[2:]
    if action == 'name':
        msg = bot.send_message(user_id, 'Введите новое имя товара')
    elif action == 'category':
        msg = get_categories('Введите новое id категории\n\n')
        msg = bot.send_message(user_id, msg)
    elif action == 'photo':
        msg = bot.send_message(user_id, 'Отправтье новое фото')
    elif action == 'price':
        msg = bot.send_message(user_id, 'Введите новую цену')
    elif action == 'description':
        msg = bot.send_message(user_id, 'Введите новое описание')
    elif action == 'del':
        msg = bot.send_message(user_id, 'Вы точно хотите удалить товар? Введите "Да" - для продолжения')
    bot.register_next_step_handler(msg, get_msg_to_edit_product, action, prod_id)




def get_msg_to_edit_product(message, action, prod_id):
    user_id = message.chat.id
    text = message.text
    msg = 'Успешно'
    user = db_file.Products.query.filter_by(prod_id=prod_id).first()
    if action == 'name':
        user.name = text
    elif action == 'category':
        user.category = text
    elif action == 'photo':
        photo_id = message.photo[-1].file_id
        save_photo(message)
        user.photo = photo_id
    elif action == 'price':
        user.price = text
    elif action == 'description':
        user.description = text
    elif action == 'del':
        if text == 'Да':
            db_file.Products.query.filter_by(prod_id=prod_id).delete()
        else:
            msg = 'Отменено'
    try:
        db_file.db.session.commit()
    except:
        msg = 'Ошибка'
    
    bot.send_message(user_id, msg)
    send_list_products(message)