from flask import Flask, request, jsonify
import mysql.connector
import os
import uuid
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API Requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API Request Latency"
)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "transactions_db")
    )

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/health", methods=["GET"])
def health():
    REQUEST_COUNT.labels("GET", "/health", "200").inc()
    return jsonify({"status": "UP"}), 200

@app.route("/transfer", methods=["POST"])
def transfer():
    start_time = time.time()

    # Simulate latency spike for SRE alert testing
    time.sleep(2)

    data = request.json
    to_account = data.get("toAccount")
    amount = data.get("amount")

    txn_id = str(uuid.uuid4())[:8]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (transaction_id, to_account, amount, status) VALUES (%s, %s, %s, %s)",
        (txn_id, to_account, amount, "SUCCESS")
    )

    conn.commit()
    cursor.close()
    conn.close()

    REQUEST_COUNT.labels("POST", "/transfer", "201").inc()
    REQUEST_LATENCY.observe(time.time() - start_time)

    return jsonify({
        "transactionId": txn_id,
        "status": "SUCCESS"
    }), 201

@app.route("/transactions", methods=["GET"])
def get_transactions():
    start_time = time.time()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transactions")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    REQUEST_COUNT.labels("GET", "/transactions", "200").inc()
    REQUEST_LATENCY.observe(time.time() - start_time)

    return jsonify(result), 200

@app.route("/simulate-failure", methods=["GET"])
def simulate_failure():
    REQUEST_COUNT.labels("GET", "/simulate-failure", "500").inc()
    return jsonify({"error": "Simulated service failure"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)