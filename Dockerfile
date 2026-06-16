FROM python:3.13-slim
LABEL authors="abatte"

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5500

CMD ["python", "app.py"]