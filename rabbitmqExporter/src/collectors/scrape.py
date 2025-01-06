import os
import requests
import logging
from src.metricType import gauge
from src.config import env

class RabbitMQMetrics:   
    @classmethod
    def initialize(cls):
        """Initialize the metrics collector with environment variables"""
        cls.host:str = env.RABBITMQ_HOST
        cls.user:str = env.RABBITMQ_USER
        cls.password:str = env.RABBITMQ_PASSWORD
        cls.base_url = f'http://{cls.host}:{env.RABBITMQ_API_PORT}/api'
        cls.session = requests.Session()
        cls.session.auth = (cls.user, cls.password)
    
    @classmethod
    def get_queue_metrics(cls):
        """Fetch metrics for all queues in all vhosts"""
        try:
            response = cls.session.get(f'{cls.base_url}/queues')
            logging.warning(response.json())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching queue metrics: {e}")
            return []
    
    @classmethod
    async def update_metrics(cls):
        """Update Prometheus metrics with current RabbitMQ queue data"""
        queues = cls.get_queue_metrics()
        for queue in queues:
            gauge.messages.labels(
                host=cls.host,
                vhost=queue['vhost'],
                name=queue['name']
            ).set(queue['messages'])
            
            gauge.messages_ready.labels(
                host=cls.host,
                vhost=queue['vhost'],
                name=queue['name']
            ).set(queue['messages_ready'])

            gauge.messages_unacknowledged.labels(
                host=cls.host,
                vhost=queue['vhost'],
                name=queue['name']
            ).set(queue['messages_unacknowledged'])
            
        logging.info(f"Updated metrics for {len(queues)} queues")