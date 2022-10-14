FROM python:3.9
WORKDIR /code
RUN apt update && apt-get install -y netcat libaio1 alien

COPY ./requirements.txt /code/requirements.txt
COPY ./requirements /code/requirements
RUN pip install --upgrade pip==22.0.0
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 80

CMD python manage.py set_data_default && \
    python manage.py collectstatic --noinput && \
    gunicorn -c gunicorn.conf.py