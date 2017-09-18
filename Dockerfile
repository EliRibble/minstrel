FROM authentise/uwsgi:10
MAINTAINER Eli Ribble <eli@authentise.com>
ADD . /src
ADD alembic.ini /etc/minstrel/alembic.ini
WORKDIR /src
RUN pip3 install -e .[develop]
EXPOSE 8000
