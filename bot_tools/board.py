from telebot import types



def admin_panel():
    panel = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton("🛍 Товары", callback_data=f'product')
    item2 = types.InlineKeyboardButton("🗂 Категории", callback_data=f'categories')
    panel.add(item1, item2)
    return panel



def products_panel():
    panel = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton("➕ Добавить", callback_data=f'add_product')
    item2 = types.InlineKeyboardButton("🖋 Редактировать", callback_data=f'edit_product')
    panel.add(item1, item2)
    return panel



def edit_product_inline(prod_id):
    panel = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton("❓ Что нужно редактировать ❓", callback_data=f'none')
    item2 = types.InlineKeyboardButton("▫️ Название ▫️", callback_data=f'edit_product_name_{prod_id}')
    item3 = types.InlineKeyboardButton("▫️ Стоимость ▫️", callback_data=f'edit_product_price_{prod_id}')
    item4 = types.InlineKeyboardButton("▫️ Категорию ▫️", callback_data=f'edit_product_category_{prod_id}')
    item5 = types.InlineKeyboardButton("▫️ Описание ▫️", callback_data=f'edit_product_description_{prod_id}')
    item6 = types.InlineKeyboardButton("▫️ Фото ▫️", callback_data=f'edit_product_photo_{prod_id}')
    item7 = types.InlineKeyboardButton("❌ Удалить ❌", callback_data=f'edit_product_del_{prod_id}')
    panel.add(item1)
    panel.add(item2, item3, item4, item5, item6, item7)
    return panel



def categories_panel():
    panel = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton("➕ Добавить", callback_data=f'add_category')
    item2 = types.InlineKeyboardButton("🖋 Редактировать", callback_data=f'edit_category')
    item3 = types.InlineKeyboardButton("❌ Удалить ❌", callback_data=f'del_category')
    panel.add(item1, item2)
    panel.add(item3)
    return panel