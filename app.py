#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pika


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/final_project/stock.db'
db = SQLAlchemy(app)
class STOCK(db.Model):
    code = db.Column(db.Text)
    key = db.Column(db.Text, primary_key=True)
    open = db.Column(db.Text)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue')


@app.route("/")
def main():
    return '''
    <br><br>Input a stock code (only support goog or aapl) and Collect data from open source api.<br>
     <form action="/collect" method="POST">
         <input name="user_input">
         <input type="submit" value="Collect!">
     </form>
     <br>
     <br>You can check stocks are recommend or not by clicking the button.
     <br>
     <form action="/get_stock" method="GET">
         <button type="submit">check stocks!</button>
     </form>
     '''

def exec_stock_strategy(code, stock_info):
    
    res = 'is not recommend'
    price = []
    for info in stock_info:
        price.append(info.open)
    if len(price) < 5:
        return ''
    if price[0] > price[1] and price[1] < price[2] and price[2] > price[3] and price[3] < price[4]:
        res = 'is recommend!!!'
    return f'{code} {res}<br>'

@app.route("/collect", methods=["POST"])
def collect():
    input_text = request.form.get("user_input", "")
    allow_data = ['goog', 'aapl']
    if input_text in allow_data:
        channel.basic_publish(exchange='',
                      routing_key='queue',
                      body=input_text)
        return "message sent !"
    return "only support goog or aapl"

@app.route("/get_stock", methods=["GET"])
def get_stock():
    allow_data = ['goog', 'aapl']
    res = ''
    for code in allow_data[:2]:
        stock_info = STOCK.query.filter_by(code=code).order_by(STOCK.key.desc()).limit(5).all()
        res += exec_stock_strategy(code, stock_info)
    if res == '':
        return 'Please add data to database first~'
    return res


@app.cli.command()
def test():
    import unittest
    import sys
 
    tests = unittest.TestLoader().discover("unit_Integration_test")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)