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
version: "3.8"

services:
  api-inserter:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: api-inserter
    environment:
      - API_URL=http://localhost:5000/books
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
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
