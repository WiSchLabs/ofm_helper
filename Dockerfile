FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ofm_helper.settings.prod
ENV OFM_USERNAME admin
ENV OFM_PASSWORD XYZ123321ZYX

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code
#COPY prod_requirements.txt /code
RUN pip3 install -r requirements.txt
#RUN pip3 install -r prod_requirements.txt

ADD . /code/
RUN mkdir database
VOLUME /code/database

RUN python3 manage.py collectstatic --no-input
RUN cp /code/core/config/test.cfg /code/core/config/prod.cfg

expose 8000
CMD /code/devops/runserver.sh -u $OFM_USERNAME -p OFM_PASSWORD
