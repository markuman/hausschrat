FROM alpine:3.12

RUN apk --update add python3 py3-pip openssh-keysign openssl
RUN pip3 install peewee bottle pexpect lesspass gunicorn

COPY main.py /opt
COPY lib/ /opt/lib
COPY start.sh /opt
RUN mkdir /opt/hausschrat
RUN chown nobody /opt/hausschrat

WORKDIR /opt
USER nobody
CMD ./start.sh

