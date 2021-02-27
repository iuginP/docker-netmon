FROM debian:buster-slim

LABEL maintainer="iugin"

# Clean output only during build
ARG DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates python3 python3-influxdb \
    apt-transport-https gnupg1 dirmngr

# Add the GPG key for Ookla's Speedtest repository
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 379CE192D401AB61

# Add the Ookla repository to our sources list
RUN echo "deb https://ookla.bintray.com/debian generic main" | tee  /etc/apt/sources.list.d/speedtest.list

# Install speedtest
RUN apt-get update && apt-get install --no-install-recommends -y \
    speedtest

# Clear the image
RUN set -e -x && \
    apt-get purge -y --auto-remove libcap2-bin && \
    rm -rf \
        /tmp/* \
        /var/tmp/* \
        /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir /app/data

COPY speedtest.py /app/speedtest.py

CMD [ "sh", "-c", "python3 speedtest.py --interval=$TEST_INTERVAL --user=$INFLUXDB_USER --password=$INFLUXDB_PASSWORD --host=$INFLUXDB_HOST --port=$INFLUXDB_PORT --database=$INFLUXDB_DATABASE" ]