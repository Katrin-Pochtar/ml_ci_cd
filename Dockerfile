FROM python:3.11-slim

WORKDIR /app
COPY main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]