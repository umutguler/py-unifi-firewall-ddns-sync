FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    cron \
    bash \
    traceroute \
    iputils-ping \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir keyrings.alt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY assets/ /app/assets/
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV CRON_MINS="*" \
    CRON_HOURS="*" \
    CRON_DAYS="*" \
    RUN_ONCE="false"

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["cron", "-f"]
