import pika
import json
import os
import time
import random

# Connection settings
credentials = pika.PlainCredentials(
    os.getenv('RABBITMQ_DEFAULT_USER', 'admin'),
    os.getenv('RABBITMQ_DEFAULT_PASS', 'password123')
)
parameters = pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_DEFAULT_HOST', 'rabbitmq'),
    credentials=credentials
)

def create_and_fill_queues():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    # Define test queues with different configurations
    queues = [
        {"name": "orders_queue", "messages": 100},
        {"name": "notifications_queue", "messages": 50},
        {"name": "email_queue", "messages": 75}
    ]
    
    try:
        for queue in queues:
            # Declare the queue
            channel.queue_declare(queue=queue["name"], durable=True)
            
            # Publish messages
            for i in range(queue["messages"]):
                message = {
                    "id": i,
                    "timestamp": time.time(),
                    "data": f"Test message {i} for {queue['name']}"
                }
                
                channel.basic_publish(
                    exchange='',
                    routing_key=queue["name"],
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Make messages persistent
                        content_type='application/json'
                    )
                )
                
            print(f"Created queue '{queue['name']}' with {queue['messages']} messages")
            
        # Create a queue with unacknowledged messages
        channel.queue_declare(queue="unacked_queue", durable=True)
        
        # Create a consumer that doesn't ack messages
        def callback(ch, method, properties, body):
            print(f" [x] Received but not acked: {body}")
            time.sleep(0.1)  # Simulate processing
            # Note: Not calling ch.basic_ack()
        
        # Publish and consume messages without acking
        for i in range(25):
            channel.basic_publish(
                exchange='',
                routing_key="unacked_queue",
                body=f"Unacked message {i}",
                properties=pika.BasicProperties(delivery_mode=2)
            )
        
        channel.basic_consume(
            queue="unacked_queue",
            on_message_callback=callback,
            auto_ack=False
        )
        
        # Start consuming briefly to create unacked messages
        channel.connection.call_later(2, channel.stop_consuming)
        channel.start_consuming()
        
    finally:
        connection.close()

if __name__ == "__main__":
    print("Setting up test queues...")
    create_and_fill_queues()
    print("Test queues setup complete!")