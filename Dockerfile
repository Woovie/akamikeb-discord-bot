FROM python:3.10.0b4

WORKDIR /pythonbot

COPY * ./

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
