FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
ffmpeg \
fontconfig \
fonts-liberation2 \
fonts-dejavu-core \
wget \
&& rm -rf /var/lib/apt/lists/* \
&& wget -q https://github.com/microsoft/cascadia-code/raw/main/ttf/static/impact.ttf -O /usr/share/fonts/truetype/impact.ttf 2>/dev/null || true \
&& fc-cache -f -v

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /models/translation
ENV ARGOS_PACKAGES_DIR=/models/translation
ENV ARGOS_INDEX_DIR=/models/translation

COPY app/ ./app/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8501
ENTRYPOINT ["/entrypoint.sh"]
