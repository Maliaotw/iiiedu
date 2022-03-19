FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD exec uwsgi --http-socket :8000 --chdir /app --wsgi-file /app/config/wsgi.py --master --processes 1 --threads 2