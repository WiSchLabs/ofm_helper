FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ofm_helper.settings.prod
ENV PHANTOM_VERSION="2.1.1"
ENV PHANTOM_JS="phantomjs-$PHANTOM_VERSION"
ENV EDITOR="vim"

RUN mkdir /code
WORKDIR /code

# Install Phantomjs
ADD scripts /code/scripts
RUN /code/scripts/download_phantomjs.sh
RUN apt-get -qq update && apt-get install -y vim cron xvfb build-essential chrpath libssl-dev libxft-dev libfreetype6 \
        libfreetype6-dev libfontconfig1 libfontconfig1-dev
RUN tar -xvf $PHANTOM_JS.tar.bz2
RUN mv $PHANTOM_JS-linux-x86_64 /usr/local/share/$PHANTOM_JS
RUN ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin

COPY requirements.txt /code
RUN pip3 install -r requirements.txt

ADD . /code/

# put current release into version file
RUN echo $(git describe --tags --always) | awk '{split($0,a,"-"); print a[1]}'
RUN echo `git describe --tags --always` | awk '{split($0,a,"-"); print a[1]}'
RUN echo $(git describe --tags --always) | awk '{split($0,a,"-"); print a[1]}' > version

# add database dir
RUN mkdir database
VOLUME /code/database

# put static files
RUN python3 manage.py collectstatic --no-input

expose 8000
CMD /code/scripts/runserver.sh
