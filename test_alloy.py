import os
import requests
from dotenv import load_dotenv

load_dotenv()

workflow_token = os.getenv("ALLOY_WORKFLOW_TOKEN")
workflow_secret = os.getenv("ALLOY_WORKFLOW_SECRET")

if not workflow_token or not workflow_secret:
    raise ValueError("Missing Alloy credentials")

url = "https://sandbox.alloy.co/v1/parameters/"

response = requests.get(
    url,
    auth=(workflow_token, workflow_secret),
    timeout=15
)

print("HTTP status:", response.status_code)
if response.status_code == 200:
    data = response.json()

    print("Required count:", len(data.get("required", [])))
    print("Optional count:", len(data.get("optional", [])))
    print("OR section type:", type(data.get("or")).__name__)
    print("Response type:", type(data).__name__)
    print("Top-level keys:", list(data.keys()))
    or_rules = data.get("or")

    print("OR section type:", type(or_rules).__name__)
    print("OR section:", or_rules)

print("\nRequired fields:")

for field in data.get("required", []):
    print(field["key"])

print("\nOptional fields:")

for field in data.get("optional", []):
    print(field["key"])

print("Response type:", type(data).__name__)

if isinstance(data, dict):
    print("Top-level keys:", list(data.keys()))
elif isinstance(data, list):
    print("Number of items:", len(data))
