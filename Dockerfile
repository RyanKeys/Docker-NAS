FROM python:3.7-slim-buster

RUN pip install flask

ADD . /app
WORKDIR /app
RUN python startup.py
ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]