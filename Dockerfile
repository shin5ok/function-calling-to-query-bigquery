FROM python:3.12.3-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

USER nobody

ENV PYTHONUNBUFFERED=on

CMD ["chainlit", "run", "main.py", "--port=8080", "--host=0.0.0.0", "--headless"]
