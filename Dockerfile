FROM python:3.13.3-alpine3.21

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY config config
COPY dagaz.py .

ARG ENV
RUN python dagaz.py "$ENV"

RUN rm -rf config
RUN rm -rf dagaz.py

COPY ansuz.py .

CMD ["uvicorn", "ansuz:app", "--host", "0.0.0.0", "--port", "8000"]
