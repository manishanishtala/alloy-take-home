# Bank X Applicant Onboarding Application

## Overview

This project is a Flask-based applicant onboarding application built as part of the Alloy Technical Success Manager take-home assignment.

The application collects applicant information, submits it to Alloy's sandbox evaluation API, and displays the resulting onboarding decision.

## Features

- Applicant onboarding form with personal and contact information
- Frontend and backend input validation
- Integration with Alloy's sandbox evaluation API
- Three supported evaluation outcomes:
  - Approved
  - Manual Review
  - Denied
- Application status page with an option to start a new application
- API credentials stored in environment variables

## Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **API Integration:** Python Requests
- **Configuration:** python-dotenv
- **Version Control:** Git

## Alloy API Integration

The application sends applicant data to:

`POST https://sandbox.alloy.co/v1/evaluations/`

The request uses HTTP Basic Authentication with Alloy workflow credentials stored in a local `.env` file.

After receiving the response, the application reads the `summary.outcome` field and displays the corresponding status to the applicant.

## Local Setup

1. Clone the repository and open the project directory.
2. Create a Python virtual environment:

   `python -m venv .venv`

3. Activate the virtual environment on Windows:

   `.venv\Scripts\Activate.ps1`

4. Install dependencies:

   `python -m pip install -r requirements.txt`

5. Create a `.env` file in the project root containing:

   `ALLOY_WORKFLOW_TOKEN=your_workflow_token`

   `ALLOY_WORKFLOW_SECRET=your_workflow_secret`

6. Start the Flask application:

   `python app.py`

7. Open `http://127.0.0.1:5000/` in your browser.

## Sandbox Testing

The application was tested against Alloy's sandbox using these last-name scenarios:

| Last Name | Expected Outcome |
|---|---|
| Smith | Approved |
| Review | Manual Review |
| Deny | Denied |

Use synthetic applicant information when testing.

## Security Considerations

- API credentials are loaded from environment variables.
- The `.env` file is excluded from Git.
- Applicant information is validated before API submission.
- Alloy API calls are made from the backend rather than directly from the browser.
- API requests include a timeout and basic error handling.

## Project Scope

This application demonstrates a simplified onboarding integration using Alloy's sandbox environment. It is intended as a take-home demonstration rather than a production banking application.