from telebot import types
from database import db_file
from bot_tools import board
from create import bot
import config





def send_list_categories(message):
    user_id = message.chat.id
    categories = db_file.Categories.query.all()
    if categories:
        msg = '🗂 Список категорий\n\n'
        for el in categories:
            msg += f'{el.categor_id}. {el.name}\n'
    else:
        msg = 'Нет категорий'
    bot.send_message(user_id, msg, reply_markup=board.categories_panel())


# ====================== ADD CATEGORY ====================== 

def add_category(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, 'Введите название ')
    bot.register_next_step_handler(msg, get_name_category)



def get_name_category(message):
    user_id = message.chat.id
    name = message.text
    db_file.add_category(name)
    bot.send_message(user_id, 'Успешно!')
    send_list_categories(message)



# ====================== EDIT CATEGORY ====================== 


def edit_category_id(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, 'Введите id категории')
    bot.register_next_step_handler(msg, get_id_category)



def get_id_category(message):
    user_id = message.chat.id
    categor_id = message.text
    msg = bot.send_message(user_id, 'Введите новое имя товара')
    bot.register_next_step_handler(msg, get_name_to_edit_product, categor_id)



def get_name_to_edit_product(message, categor_id):
    user_id = message.chat.id
    text = message.text
    msg = 'Успешно'
    category = db_file.Categories.query.filter_by(categor_id=categor_id).first()
    try:
        category.name = text
        db_file.db.session.commit()
    except:
        msg = 'Ошибка'
    
    bot.send_message(user_id, msg)
    send_list_categories(message)



def del_category_id(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, 'Введите id категории')
    bot.register_next_step_handler(msg, get_id_category_to_del)


def get_id_category_to_del(message):
    user_id = message.chat.id
    categor_id = message.text
    msg = 'Успешно'
    try:
        db_file.Categories.query.filter_by(categor_id=categor_id).delete()
        db_file.db.session.commit()
    except:
        msg = 'Ошибка'
    bot.send_message(user_id, msg)
    send_list_categories(message)