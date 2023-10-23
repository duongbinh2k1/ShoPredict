FROM python:3.10

WORKDIR /crawler

COPY requirements.txt /crawler
COPY . /crawler

RUN pip install --no-cache-dir -r requirements.txt
# CMD ["python", "crawler.py"]