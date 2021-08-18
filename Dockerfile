FROM python:3.9.6-buster

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 manage:app
