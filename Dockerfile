FROM python:3.12.5

WORKDIR /app

COPY requirements.txt .
RUN pip install -r --no-cache-dir requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
