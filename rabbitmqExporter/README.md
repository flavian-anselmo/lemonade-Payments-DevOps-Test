# RABBITMQ EXPORTER 

## Metric Overview

### Total Messages in Queue
```python
messages = Gauge(
    'rabbitmq_individual_queue_messages',
    'Total number of messages in queue',
    ['host', 'vhost', 'name']
)
```

### Ready Messages in Queue
```python
messages_ready = Gauge(
    'rabbitmq_individual_queue_messages_ready',
    'Total number of messages ready in queue',
    ['host', 'vhost', 'name']
)
```

### Unacknowledged Messages in Queue
```python
messages_unacknowledged = Gauge(
    'rabbitmq_individual_queue_messages_unacknowledged',
    'Total number of messages unacknowledged in queue',
    ['host', 'vhost', 'name']
)
```

## Label Descriptions

Each metric uses three labels for precise queue identification:

**host**
- Description: RabbitMQ node hostname
- Example: `rabbitmq-prod-01`

**vhost**
- Description: Virtual host name
- Example: `/` or `my-vhost`

**name**
- Description: Queue name
- Example: `orders-queue`

## Common Queries

### Basic Queue Monitoring Example
```promql
# HELP rabbitmq_individual_queue_messages Total number of messages in queue
# TYPE rabbitmq_individual_queue_messages gauge
rabbitmq_individual_queue_messages{host="rabbitmq",name="email_queue",vhost="/"} 2400.0
rabbitmq_individual_queue_messages{host="rabbitmq",name="notifications_queue",vhost="/"} 1600.0
rabbitmq_individual_queue_messages{host="rabbitmq",name="orders_queue",vhost="/"} 3200.0
rabbitmq_individual_queue_messages{host="rabbitmq",name="unacked_queue",vhost="/"} 800.0
# HELP rabbitmq_individual_queue_messages_ready Total number of messages ready in queue
# TYPE rabbitmq_individual_queue_messages_ready gauge
rabbitmq_individual_queue_messages_ready{host="rabbitmq",name="email_queue",vhost="/"} 2400.0
rabbitmq_individual_queue_messages_ready{host="rabbitmq",name="notifications_queue",vhost="/"} 1600.0
rabbitmq_individual_queue_messages_ready{host="rabbitmq",name="orders_queue",vhost="/"} 3200.0
rabbitmq_individual_queue_messages_ready{host="rabbitmq",name="unacked_queue",vhost="/"} 0.0
# HELP rabbitmq_individual_queue_messages_unacknowledged Total number of messages unacknowledged in queue
# TYPE rabbitmq_individual_queue_messages_unacknowledged gauge
rabbitmq_individual_queue_messages_unacknowledged{host="rabbitmq",name="email_queue",vhost="/"} 0.0
rabbitmq_individual_queue_messages_unacknowledged{host="rabbitmq",name="notifications_queue",vhost="/"} 0.0
rabbitmq_individual_queue_messages_unacknowledged{host="rabbitmq",name="orders_queue",vhost="/"} 0.0
rabbitmq_individual_queue_messages_unacknowledged{host="rabbitmq",name="unacked_queue",vhost="/"} 800.0
```

## Setup  .conf file 
```bash
[exporter]
EXPORTER_PORT=9125

[rabbitmq]
RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=password123
RABBITMQ_API_PORT=15672

```


## How to configure Prometheus to Allow Periodic Monitoring 
```bash
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: prometheus
   static_configs:
    - targets:
       - prometheus:9090

 - job_name: rabbitmq
   static_configs:
    - targets: ['rabbitmq-exporter:9125']
   scrape_interval: 30s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
rule_files:
  - '/etc/prometheus/rules.yml'
```


## Alerting Configuration

```yaml
# Example alert rules
groups:
- name: RabbitMQ Queue Alerts
  rules:
  - alert: QueueBacklogGrowing
    expr: rate(rabbitmq_individual_queue_messages[5m]) > 0.5
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: Queue backlog increasing
      
  - alert: HighUnackedMessages
    expr: rabbitmq_individual_queue_messages_unacknowledged > 1000
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: High number of unacknowledged messages
```
## How to run the exporter using docker 

```bash 
docker compose build 

docker compose up -d 
```

## To simulate RabbitMq scripts, I created a script to create queues and messages 
Below are the queues to be created 
```bash
 queues = [
        {"name": "orders_queue", "messages": 100},
        {"name": "notifications_queue", "messages": 50},
        {"name": "email_queue", "messages": 75}
    ]
```

### Performance Optimization
- Monitor consumer utilization
- Track message age in queue




