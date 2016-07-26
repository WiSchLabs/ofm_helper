FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ofm_helper.settings.prod
ENV PHANTOM_VERSION="2.1.1"
ENV PHANTOM_JS="phantomjs-$PHANTOM_VERSION"
ENV EDITOR="vim"

RUN mkdir /code
WORKDIR /code

# Install Phantomjs
RUN apt-get -qq update && apt-get install -y vim cron xvfb build-essential chrpath libssl-dev libxft-dev libfreetype6 \
        libfreetype6-dev libfontconfig1 libfontconfig1-dev
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS-linux-x86_64.tar.bz2 -O $PHANTOM_JS.tar.bz2
RUN tar -xvf $PHANTOM_JS.tar.bz2
RUN mv $PHANTOM_JS-linux-x86_64 /usr/local/share/$PHANTOM_JS
RUN ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin

COPY requirements.txt /code
#COPY prod_requirements.txt /code
RUN pip3 install -r requirements.txt
#RUN pip3 install -r prod_requirements.txt

ADD . /code/
RUN mkdir database
VOLUME /code/database

RUN python3 manage.py collectstatic --no-input

# Add cronjobs for parsing
RUN line="*/5 * * * * /code/scripts/run_cron_jobs.sh"
RUN (crontab -u root -l; echo "$line" ) | crontab -u root -

#expose 8000
#CMD /code/scripts/runserver.sh
