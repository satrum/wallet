#FROM python:3.7
#ADD . /code
#WORKDIR /code
#RUN pip install -r requirements.txt
#CMD python wsgi.py

FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]

