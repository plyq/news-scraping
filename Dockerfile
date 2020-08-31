FROM python:3.7-alpine

RUN apk --update add \
         g++ gcc libxslt-dev py-lxml \
    && rm -rf /var/cache/apk/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python", "entrypoint.py"]
