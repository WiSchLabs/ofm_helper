FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ofm_helper.settings.prod

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code
COPY prod_requirements.txt /code
RUN pip3 install -r requirements.txt
RUN pip3 install -r prod_requirements.txt

ADD . /code/
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input

RUN cp /code/core/config/test.cfg /code/core/config/prod.cfg

expose 8000
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
