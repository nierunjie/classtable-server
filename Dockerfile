FROM alpine:latest
MAINTAINER LANTHORA
RUN apk add python3 py3-pip
RUN pip3 install requests Flask beautifulsoup4
EXPOSE 5000
COPY . /app
WORKDIR /app
ENTRYPOINT python3 app.py