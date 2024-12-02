from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from pymongo import MongoClient
from tasks import process_book_task  # Import task function

app = Flask(__name__)

# Redis setup
redis_client = Redis(host='redis', port=6379, decode_responses=True)

# RQ Queue setup
task_queue = Queue(connection=redis_client)

# MongoDB setup
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["bookstore"]
books_collection = db["books"]

# Enqueue book processing task
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    # Enqueue the task
    job = task_queue.enqueue(process_book_task, data)

    return jsonify({"message": "Book task added to queue", "job_id": job.id}), 202

# Get the status of a task by job ID
# @app.route('/tasks/<job_id>', methods=['GET'])
# def get_task_status(job_id):
#     from rq.job import Job
#     try:
#         job = Job.fetch(job_id, connection=redis_client)
#     except Exception as e:
#         return jsonify({"error": "Job not found or has expired", "details": str(e)}), 404

#     return jsonify({
#         "id": job.id,
#         "status": job.get_status(),
#         "result": job.result
#     })

# Fetch all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = list(books_collection.find({}, {"_id": 0}))
    return jsonify(books), 200

# Fetch a single book by ID
@app.route('/books/<book_id>', methods=['GET'])
def get_single_book(book_id):
    book = books_collection.find_one({"id": book_id}, {"_id": 0})
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
