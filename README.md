---

# **API Bulk Data Insertion Script (Dockerized)**

This repository contains a Dockerized Python application to automate bulk data insertion into an API. It uses Python with Docker to provide a portable and consistent environment.

---

## **Features**

- Bulk insertion of 1000 records into an API using Python.
- Dockerized environment for easy setup and portability.
- Customizable API endpoint and payload structure.
- Handles success and failure responses.

---

## **Docker Files**

### **1. Dockerfile**
Defines the Python environment and installs dependencies.

```dockerfile
# Use official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entrypoint
CMD ["python", "api_insert_books.py"]
```

---

### **2. `docker-compose.yml`**

Defines the service configuration for running the application.

```yaml
version: '1.0'

services:
  flask_app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    networks:
      - app_network
    depends_on:
      - mongodb
      - redis

  mongodb:
    image: mongo:latest
    container_name: mongo_db
    ports:
      - "27017:27017"
    networks:
      - app_network

  redis:
    image: redis:latest
    container_name: redis_cache
    ports:
      - "6379:6379"
    networks:
      - app_network

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: python worker.py
    deploy:
      replicas: 5
    networks:
      - app_network
    depends_on:
      - redis
      - flask_app

  # To monitor queue but currently facing issue
  rq_dashboard:
    image: eoranged/rq-dashboard
    ports:
      - "9181:9181"
    environment:
      - RQ_DASHBOARD_REDIS_HOST=redis
      - RQ_DASHBOARD_REDIS_PORT=6379
    depends_on:
      - redis
    networks:
      - app_network

networks:
  app_network:
    driver: bridge
```

---

## **Setup and Usage**

1. Clone the repository:
   ```bash
   git clone https://github.com/singhrahul8290/python-redis-queue-project.git
   cd your-repo
   ```

2. Build the Docker image:
   ```bash
   docker-compose build
   ```

3. Run the container:
   ```bash
   docker-compose up
   ```

4. The script will:
   - Send 1000 `POST` requests to the API.
   - Print the status of each request (success or failure).
   - Summarize the results at the end.

---

## **Configuration**

- The API endpoint can be updated by modifying the environment variable `API_URL` in `docker-compose.yml`.
- To change the payload structure or the number of requests, update the script:
  - Payload structure:
    ```python
    def generate_payload(index):
        return {
            "id": str(index),
            "title": f"Book {index}"
        }
    ```
  - Number of requests:
    ```python
    execute_requests(total_requests=1000)
    ```

---

## **Example Output**

After running the container, you should see output similar to:
```bash
api-inserter  | Request 1: Success - {'message': 'Book inserted successfully'}
api-inserter  | Request 2: Failed - {'error': 'Duplicate entry'}
api-inserter  | ...
api-inserter  | Total Requests: 1000
api-inserter  | Successful Requests: 950
api-inserter  | Failed Requests: 50
```

---

## **Stopping the Application**

To stop the running container:
```bash
docker-compose down
```

---

## **Contributing**

Contributions are welcome! Fork the repository, make changes, and submit a pull request.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---
