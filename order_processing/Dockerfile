FROM python:3.12.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app/ app/
COPY main.py main.py

CMD ["python", "main.py"]