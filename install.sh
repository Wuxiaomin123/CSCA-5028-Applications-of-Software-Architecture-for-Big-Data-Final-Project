sqlite3 stock.db "PRAGMA database_list;"
sqlite3 stock.db "CREATE TABLE stock(code text NOT NULL, key text NOT NULL PRIMARY KEY, open text NOT NULL);"
python3 worker.py > worker.log &
gunicorn app:app --worker-class eventlet
