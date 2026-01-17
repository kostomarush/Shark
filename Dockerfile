FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      net-tools \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      nmap git ca-certificates \
      libpq5 \
      bash \
 && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/scipag/vulscan /tmp/vulscan \
 && mkdir -p /usr/share/nmap/scripts \
 && mv /tmp/vulscan /usr/share/nmap/scripts/vulscan \
 && rm -rf /tmp/vulscan

COPY resource/update_cve.csv /usr/share/nmap/scripts/update_cve.csv

COPY --from=builder /usr/local /usr/local

COPY . /app
RUN chmod +x /app/start.sh

EXPOSE 8080 51000
CMD ["bash", "/app/start.sh"]