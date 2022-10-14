FROM python:3.8.10

WORKDIR /code
COPY requirements.txt .
RUN apt-get update \
  && apt-get -y install tesseract-ocr
RUN pip install -r requirements.txt
COPY application application
COPY DAO DAO
COPY migrations migrations
COPY services services
COPY views views
COPY db_config.py .
COPY implemented.py .
COPY app.py .
 
CMD gunicorn -b 0.0.0.0:5000 -w 4 app:app # flask run --host=0.0.0.0
