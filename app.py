import os
from urllib import response
from urllib import response
from dotenv import load_dotenv
import requests 
from flask import Flask, render_template, request
from datetime import datetime
load_dotenv()
ALLOY_EVALUATION_URL = "https://sandbox.alloy.co/v1/evaluations/"
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "We were esablished in 1990 and have been serving our customers ever since."

@app.route("/contact")
def contact():
    return "You can reach us at 800-555-5555 or email us at contact@bankx.com"

@app.route("/submit", methods=["POST"])
def submit_application():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    address_line_1 = request.form.get("address_line_1")
    address_line_2 = request.form.get("address_line_2") or ""
    city = request.form.get("city")
    state = request.form.get("state")
     # Validate state
    if not state or not state.isalpha() or len(state) != 2:
        return "Invalid state. Please enter a two-letter code.", 400
    zip_code = request.form.get("zip_code")
    country = request.form.get("country")
    if not country or country != "US":
        return "Invalid country. We are only considering applications from the US.", 400
    date_of_birth = request.form.get("date_of_birth")
    if not date_of_birth:
        return "Date of birth is required.", 400
    try :
        parsed_dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        if parsed_dob.date() >= datetime.now().date():
            return "Invalid date of birth. Please enter a date in the past.", 400
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400

    if parsed_dob.strftime("%Y-%m-%d") != date_of_birth:
            return "Invalid date format. Please use YYYY-MM-DD.", 400
    phone = request.form.get("phone")

    if not phone or len(phone) != 10 or not phone.isdigit():
        return "Invalid phone number. Please enter a 10-digit number.", 400
    ssn = request.form.get("ssn")
    if not ssn or len(ssn) != 9 or not ssn.isdigit():
        return "Invalid SSN. Please enter a 9-digit number.", 400
    
    applicant_data = {
    "name_first": first_name,
    "name_last": last_name,
    "email_address": email,
    "address_line_1": address_line_1,
    "address_line_2": address_line_2,
    "address_city": city,
    "address_state": state,
    "address_country_code": country,
    "address_postal_code": zip_code,
    "birth_date": date_of_birth,
    "phone_number": phone,
    "document_ssn": ssn
    }

    workflow_token = os.getenv("ALLOY_WORKFLOW_TOKEN")
    workflow_secret = os.getenv("ALLOY_WORKFLOW_SECRET")

    if not workflow_token or not workflow_secret:
        return "Evaluation service is not configured.", 503
    
    try:
        response = requests.post(
            ALLOY_EVALUATION_URL,
            auth=(workflow_token, workflow_secret),
            json=applicant_data,
            timeout=15
        )
    except requests.exceptions.RequestException:
        return "Unable to contact the evaluation service.", 503

    if response.status_code not in (200, 201):
        return "Alloy evaluation request was unsuccessful.", 502
    result = response.json()

    summary = result.get("summary", {})
    outcome = summary.get("outcome")

    if outcome == "Approved":
        return render_template("results.html", message="Congratulations! Your application has been approved."), 200
    elif outcome == "Manual Review":
        return render_template("results.html", message="Your application requires further review. Please wait for our team to contact you."), 200
    elif outcome == "Denied":
        return render_template("results.html", message="We're unable to approve your application."), 200
    else:
        return render_template("results.html", message="Your application requires further processing."), 200

    print("Summary type:", type(summary).__name__)

    
    if isinstance(summary, dict):
        print("Summary keys:", list(summary.keys()))
        print("Evaluation result:", summary.get("result"))
        print("Evaluation outcome:", summary.get("outcome"))

    print("Response type:", type(result).__name__)

    if isinstance(result, dict):
        print("Response keys:", list(result.keys()))
    return "Alloy evaluation request completed.", 200

if __name__ == "__main__":
    app.run(debug=True)