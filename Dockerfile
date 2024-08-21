# to build this image:
# docker build -t aufent:v5 .
# to run the docker container:
# docker run -d --name aufent aufent:v5

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY main.py /app/
COPY requirements.txt /app/
COPY entrypoint.sh /app/

RUN apk add --no-cache \
    firefox-esr \
    && wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz" -O geckodriver.tar.gz \
    && tar -xzf geckodriver.tar.gz -C /usr/local/bin/ \
    && rm geckodriver.tar.gz \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && chmod +x /app/main.py /app/entrypoint.sh  \
    && ln -s /usr/bin/firefox-esr /usr/bin/firefox \
    && rm -rf /var/cache/apk/* /root/.cache/pip

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
