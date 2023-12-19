FROM python:3.9-slim-buster

WORKDIR /app
RUN apt-get update \
      && apt-get install -y --no-install-recommends \
      --no-install-suggests build-essential \
      && pip install --no-cache-dir --upgrade pip 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 9000

CMD ["sh", "-c", "python3.9 main.py"]