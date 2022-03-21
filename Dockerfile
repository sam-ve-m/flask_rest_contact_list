FROM python:3.8

COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt

COPY ./.env /api
COPY ./app.py /api
COPY ./src /api/src
COPY ./flask-restful /api/flask-restful

ENTRYPOINT ["python"]
CMD ["app.py"]
