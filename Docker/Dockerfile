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


