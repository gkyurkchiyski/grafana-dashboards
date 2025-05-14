Using Node Exporter as data collector and Prometheus as data source. Node Exporter is collecting all key rource metrics and it exposes that data 
on an endpoint that Prometheus will then scrape and provide to Grafana when Grafana queries Prometheus. Created Grafana dashboards for monitoring 
system/VM key resource usage then exporting dashboards from the local Grafana instance using Python script.
