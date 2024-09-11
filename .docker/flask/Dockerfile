FROM alpine:3.18

WORKDIR /usr/src/app

RUN apk add --no-cache \
        pcre \
        uwsgi-python3 \
        python3 \
        py3-pip


COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uwsgi", "--ini", "flask.ini"]