FROM ubuntu:18.04

#ARG CACHEBUST

RUN echo 1 && apt-get update && apt-get install -y apt-utils sudo


RUN adduser --disabled-password --gecos "snetservice user" top && \
	adduser top sudo && \
	echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER top

#RUN whoami

RUN sudo apt-get install -y git \
	build-essential \
	python3.6 \
	python3.6-dev \
	python3-pip

RUN sudo apt-get install -y wget curl vim


WORKDIR /home/top/

RUN curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6

RUN pip --version


WORKDIR /tmp

COPY requirements.txt /tmp/
RUN sudo pip install -r requirements.txt
RUN echo 1
RUN python3.6 -m nltk.downloader all

RUN sudo apt-get install -y supervisor && \
    sudo rm /etc/supervisor/supervisord.conf

COPY requirements_2.txt /tmp/
RUN sudo pip install -r requirements_2.txt

RUN sudo mkdir /var/log/kovand/ \
    /var/log/ropstend/ \
    /var/log/topic_grpc/ \
    /var/log/topic_rest/

RUN mkdir /home/top/pay/ \
    /home/top/daemons/ \
    /home/top/pay/kovan/ \
    /home/top/pay/ropsten/ \
    /home/top/gunicorn/ \
    /home/top/daemons/kovan/ \
    /home/top/daemons/ropsten/

ENV DAEMON_VERSION 0.1.6

RUN wget -O snet-daemon.tar.gz https://github.com/singnet/snet-daemon/releases/download/v$DAEMON_VERSION/snet-daemon-v$DAEMON_VERSION-linux-amd64.tar.gz && \
    tar  --strip-components=1 -xzf snet-daemon.tar.gz && \
    cp snetd /home/top/daemons/kovan/ && \
    cp snetd /home/top/daemons/ropsten/

RUN echo 22

COPY daemons/snetd_topic_kovan.json /home/top/daemons/kovan/
COPY daemons/snetd_topic_ropsten.json /home/top/daemons/ropsten/
COPY gunicorn/config.py /home/top/gunicorn/
#COPY supervisor/kovand.conf /etc/supervisor/conf.d/
#COPY supervisor/ropstend.conf /etc/supervisor/conf.d/
COPY supervisor/topic_grpc.conf /etc/supervisor/conf.d/
COPY supervisor/topic_rest.conf /etc/supervisor/conf.d/
COPY supervisor/supervisord.conf /etc/supervisor/


WORKDIR /home/top/
RUN mkdir dep
WORKDIR /home/top/dep

#RUN git clone https://github.com/singnet/network-analytics-services.git && \
#	cd network-analytics-services

RUN whoami

RUN echo 13 && \
	git clone https://github.com/edyirdaw/topic-analysis.git && cd topic-analysis &&  git checkout --track origin/dev

WORKDIR /home/top/dep/topic-analysis

RUN pwd
RUN python3.6 -m grpc_tools.protoc -I. --python_out=.  --grpc_python_out=. service_spec/topic_analysis.proto

#CMD ["/usr/bin/supervisord"]

#RUN sudo service supervisor stop
#RUN sudo service supervisor start


