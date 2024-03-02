FROM python:3.9

# mount dir
RUN mkdir -p /opt/mnt
WORKDIR /opt/mnt

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y curl

ADD requirements.txt ./
RUN pip install -r requirements.txt

RUN curl -sL https://github.com/geolonia/japanese-addresses/archive/refs/heads/master.tar.gz | tar xvfz - -C /tmp/

# expose port
EXPOSE 8888