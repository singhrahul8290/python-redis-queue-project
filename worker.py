from redis import Redis
from rq import Worker, Queue
import tasks 

# Connect to Redis
redis_conn = Redis(host='redis', port=6379)

if __name__ == "__main__":
    listen = ['default']  # Queue to listen to
    worker = Worker(Queue(name=listen[0], connection=redis_conn))
    worker.work()
