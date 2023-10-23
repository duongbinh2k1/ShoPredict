FROM apache/airflow:2.7.0-python3.10

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    heimdal-dev \
    openjdk-11-jre-headless \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
RUN pip uninstall -y argparse