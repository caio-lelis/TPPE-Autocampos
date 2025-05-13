FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev dos2unix && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN if [ -f entrypoint.sh ]; then dos2unix entrypoint.sh && chmod +x entrypoint.sh; fi

EXPOSE 8009

CMD ["python", "app.py"]  # Ou ["/app/entrypoint.sh"]