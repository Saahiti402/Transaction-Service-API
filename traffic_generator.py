import requests
import time
import random

BASE_URL = "http://localhost:5000"

def generate_health_check():
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health:", response.status_code)
    except Exception as e:
        print("Health Error:", e)

def generate_transfer():
    try:
        payload = {
            "toAccount": str(random.randint(1000000000, 9999999999)),
            "amount": random.randint(100, 5000)
        }

        response = requests.post(
            f"{BASE_URL}/transfer",
            json=payload
        )
        print("Transfer:", response.status_code, response.json())
    except Exception as e:
        print("Transfer Error:", e)

def generate_transactions_check():
    try:
        response = requests.get(f"{BASE_URL}/transactions")
        print("Transactions:", response.status_code)
    except Exception as e:
        print("Transactions Error:", e)

def generate_metrics_check():
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        print("Metrics:", response.status_code)
    except Exception as e:
        print("Metrics Error:", e)

def generate_failure_traffic():
    try:
        response = requests.get(f"{BASE_URL}/simulate-failure")
        print("Failure:", response.status_code)
    except Exception as e:
        print("Failure Error:", e)

if __name__ == "__main__":
    while True:
        # normal traffic
        generate_health_check()
        generate_transfer()
        generate_transactions_check()
        generate_metrics_check()

        # occasional failure traffic
        if random.random() < 0.3:   # 30% chance
            generate_failure_traffic()

        # variable traffic interval
        time.sleep(random.uniform(0.5, 2))