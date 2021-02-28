# Docker NetMon

This is project provides a docker image to monitor your internet connection.
It also provides a basic docker-compose configuration for a standalone system that collects, stores and displays the bandwidth using speedtest.net, influxdb, grafana.

## Download

To clone the project:

```shell
git clone https://github.com/iuginP/docker-netmon.git
cd docker-netmon
```

## Execution

To run NetMon:

```shell
docker-compose up -d --build
```

To connect to grafana go to http://localhost:3000

## Grafana configuration

Create and set the right permissions to the grafana data dir:

```shell
mkdir -p grafana_data/data/grafana/
sudo chown -R 472:1 grafana_data/data/grafana/
```

Grafana will require to be configured the first time the project is executed. The default credentials are:
* username: admin
* password: admin

To display the default dashboard, you need to import it from: https://github.com/iuginP/docker-netmon/blob/master/grafana_speedtest_dashboard.yaml
