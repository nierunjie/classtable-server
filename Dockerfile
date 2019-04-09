FROM alpine:latest
MAINTAINER LANTHORA
RUN apk add python3 py3-pip py3-lxml
RUN pip3 install requests Flask beautifulsoup4
COPY . /app
WORKDIR /app
ENTRYPOINT python3 app.py