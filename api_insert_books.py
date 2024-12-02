import requests
import time

API_URL = "http://localhost:5000/books"

def generate_payload(index):
    return {
        "id": str(index),
        "title": f"Book {index}"
    }

HEADERS = {
    "Content-Type": "application/json",
}

def send_request(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return None, str(e)

def execute_requests(total_requests=1000):
    success_count = 0
    failure_count = 0
    for i in range(1, total_requests + 1):
        payload = generate_payload(i)
        status, result = send_request(payload)
        if status == 202:
            success_count += 1
            print(f"Request {i}: Success - {result}")
        else:
            failure_count += 1
            print(f"Request {i}: Failed - {result}")
        time.sleep(0.05)
    print(f"\nTotal Requests: {total_requests}")
    print(f"Successful Requests: {success_count}")
    print(f"Failed Requests: {failure_count}")

if __name__ == "__main__":
    execute_requests(500)
