from flask import render_template, request
from web_app.utils import parse_init_data
from database import db_file
from bot_tools import wa_request
from create import app
import config



@app.route('/')
def index():
    products = db_file.Products.query.all()
    categories = db_file.Categories.query.all()
    return render_template('index.html', products=products, categories=categories)



@app.post('/sendMessage')
def submit_order():
    data = request.json
    init_data = parse_init_data(token=config.BOT_TOKEN, raw_init_data=data['initData'])
    if init_data is False:
        return False
    wa_request.wa_send_message(data, init_data)
    return ''


def main():
    app.run(host=config.WEBAPP_HOST, port=config.WEBAPP_PORT, debug=True)


if __name__ == "__main__":
    main()