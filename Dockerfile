FROM ubuntu:20.04
RUN apt update
RUN apt -y install python3-pip sqlite3
RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install numpy pandas matplotlib flask flask_sqlalchemy gunicorn eventlet yfinance pandas==1.5.3 pika Flask-Testing


WORKDIR /home/final_project
