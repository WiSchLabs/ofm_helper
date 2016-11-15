FROM python:3-onbuild

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ofm_helper.settings.prod
ENV EDITOR="vim"

WORKDIR /usr/src/app

# put current release into version file
#RUN git fetch --tags
#RUN git describe --tags --always | awk '{split($0,a,"-"); print a[1]}'
#RUN git describe --tags --always | awk '{split($0,a,"-"); print a[1]}' > version
RUN echo "0.0.1" > version

# migrate database to current structure
RUN mkdir logs

# put static files
RUN python3 manage.py collectstatic --no-input

CMD ["gunicorn", "-c", "gunicorn_conf.py", "ofm_helper.wsgi"]