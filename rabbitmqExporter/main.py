from prometheus_client import make_asgi_app
from hypercorn.asyncio import serve
import asyncio
import logging
from hypercorn.config import Config
from src.collectors.scrape import RabbitMQMetrics
from src.config import env


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RabbitMQMetrics.initialize()

async def collect():
    await RabbitMQMetrics.update_metrics()
    logger.info('collecting metrics....')

    
async def metrics_app(scope,receive, send):
    if scope['type'] == 'http' and scope['path'] == f'/metrics':
        await collect()
    app = make_asgi_app()
    await app(scope, receive, send)

async def main():
    hypercon_config = Config()
    hypercon_config.bind = [f"0.0.0.0:{env.EXPORTER_PORT}"]
    await serve(metrics_app, hypercon_config)

if __name__ == '__main__':
    asyncio.run(main())