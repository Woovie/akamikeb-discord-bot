FROM python:latest

WORKDIR /pythonbot

COPY * ./

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
