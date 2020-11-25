FROM alpine:3.12

RUN apk --update add python3 py3-pip openssh-keysign
RUN pip3 install peewee bottle pexpect lesspass
COPY main.py /opt
COPY lib/ /opt/lib
RUN mkdir /opt/hausschrat
RUN chown nobody /opt/hausschrat

WORKDIR /opt
USER nobody
CMD python3 main.py
