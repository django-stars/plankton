FROM ubuntu:16.04
MAINTAINER Dmytro Upolovnikov <dmitry.upolovnikov@djangostars.com>

RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y python3 python3-pip wkhtmltopdf xvfb

COPY . /home/app/plankton
RUN cd /home/app/plankton/ && python3 setup.py install
EXPOSE 8080

ENTRYPOINT plankton-server --port 8080 --wkhtmltopdf_command "xvfb-run -a wkhtmltopdf"

