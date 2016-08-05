FROM ubuntu:16.04
MAINTAINER Dmytro Upolovnikov <dmitry.upolovnikov@djangostars.com>

RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y python3 python3-pip wkhtmltopdf xvfb

COPY plankton /home/app/plankton
COPY requirements.txt /home/app/plankton/requirements.txt

RUN pip3 install -r /home/app/plankton/requirements.txt
EXPOSE 8080
ENTRYPOINT python3 /home/app/plankton/plankton_server.py --port 8080 --wkhtmltopdf_command "xvfb-run -a wkhtmltopdf"

