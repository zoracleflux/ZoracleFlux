FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ZORACLEFLUX_DATA_DIR=/data

WORKDIR /opt/zoracleflux
COPY . /opt/zoracleflux
RUN pip install --no-cache-dir --no-deps . \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin zoracleflux \
    && mkdir -p /data \
    && chown -R 10001:10001 /opt/zoracleflux /data

USER 10001:10001
VOLUME ["/data"]
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python /opt/zoracleflux/support/production/healthcheck.py --root /opt/zoracleflux --db /data/pilot.sqlite3

ENTRYPOINT ["zoracleflux"]
CMD ["pilot", "--database", "/data/pilot.sqlite3", "--runs", "1", "--json"]
