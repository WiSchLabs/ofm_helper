FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ofm_helper.settings.prod
ENV OFM_USERNAME XXX
ENV OFM_PASSWORD 1234

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
RUN sed -i 's/XXX/$OFM_USERNAME/' /code/core/config/prod.cfg
RUN sed -i 's/1234/$OFM_PASSWORD/' /code/core/config/prod.cfg

RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'pass')" | python3 manage.py shell

expose 8000
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
