FROM python:3.8-slim

RUN mkdir /test

WORKDIR /test

COPY requirements.txt /test

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /web_app /test/web_app
COPY /static /test/static
COPY /tg_client /test/tg_client
COPY /wildberries /test/wildberries
COPY /db /test/db

ENV PHONE=12345550
ENV API_ID=292210192
ENV API_HASH=afdsfhhdsofojdsk
ENV TEST=False

CMD ["uvicorn", "web_app.main:app", "--host=0.0.0.0", "--port=8000"]