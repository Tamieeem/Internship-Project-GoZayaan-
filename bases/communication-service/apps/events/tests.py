from celery import Celery


app = Celery('dummy_service', broker='amqp://guest:guest@localhost:5672//')


payload = {
    "template_code": "12345",  
    "template_type": "EMAIL",
    "delivery_type": "EMAIL",
    "priority": "instant",     
    "to_contact": ["eyasinbhui@gmail.com"],
    "variables": {"name": "Test", "otp": "9876"},
    "region": "BD",
    "service": "GOZAYAAN"
}

print("Pushing message directly to RabbitMQ...")


result = app.send_task(
    'apps.events.tasks.receive_instant_task', 
    args=[payload], 
    queue='instant'
)

print(f"✅ Message sent directly to Queue! Task ID: {result.id}")