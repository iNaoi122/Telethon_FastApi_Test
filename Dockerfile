FROM python:3.8-slim

RUN mkdir /test

WORKDIR /test

COPY requirements.txt /test

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /web_app /test/web_app
COPY /static /test/static

EXPOSE 8000:8079

CMD ["uvicorn", "web_app.main:app", "--host=0.0.0.0", "--port=8000"]