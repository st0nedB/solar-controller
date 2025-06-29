FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN python -m pip install -r /app/requirements.txt

CMD ["python3 main.py"]