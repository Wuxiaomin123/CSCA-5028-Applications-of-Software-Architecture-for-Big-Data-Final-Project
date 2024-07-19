import pika
import sqlite3
import yfinance as yf
import pandas as pd

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue')

def callback(ch, method, properties, body):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    code = body.decode('utf-8')
    print(f'download {code} data')
    df = yf.Ticker(code).history(period="5d")
    df = df.reset_index()
    df = df[['Date', 'Open']]
    data = []
    for i in df.values.tolist():
        date = str(i[0]).split(' ')[0]
        open = str(i[1])
        data.append((code, date+code, open))
    cursor.executemany('INSERT OR IGNORE INTO stock (code, key, open) VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()


channel.basic_consume('queue', callback, True)
channel.start_consuming()