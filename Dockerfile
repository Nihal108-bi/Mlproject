FROM python:3.8-slim-bookworm

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y awscli
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
