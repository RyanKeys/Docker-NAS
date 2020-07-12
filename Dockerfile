FROM python:3.7-slim-buster

RUN pip install flask

ADD . /app

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
RUN python3 first_time_setup.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]