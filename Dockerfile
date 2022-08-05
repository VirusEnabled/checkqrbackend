FROM python:3.9
WORKDIR /code
RUN apt update && apt-get install -y netcat libaio1 alien

COPY ./requirement.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 80

CMD python manage.py set_data_default && \
    python manage.py collectstatic --noinput && \
    gunicorn -c gunicorn.conf.py