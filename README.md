# Kapture Finance Voice AI Collections Agent

## Overview

This project is a working Voice AI collections agent built for the Kapture AI Delivery Intern take-home assignment.

The assistant, **Maya**, handles outbound collections conversations for overdue loan EMIs.

The demo customer is:

* Name: Rahul Sharma
* Loan Type: Personal Loan
* Overdue EMI: INR 8,499
* Days Past Due: 12

The main focus of the project is safe customer authentication, collections conversation handling, tool calling, and privacy guardrails.

---

## Architecture

The system follows this flow:

Customer Voice
→ Vapi Telephony / Web Call
→ Speech-to-Text
→ GPT-based Voice Agent
→ Tool/API Calls
→ FastAPI Backend
→ Tool Response
→ Text-to-Speech
→ Customer

The backend is exposed during development using ngrok.

---

## Voice AI Stack

### Voice Platform

Vapi

### Model

GPT-4.1

Chosen because it provides strong instruction following and reliable tool-calling behavior for a multi-step collections conversation.

### Transcriber

Soniox STT RT v5

Used for low-latency speech-to-text transcription.

### Voice

Vapi Elliot v2

Chosen for natural conversational speech and low latency.

---

## Core Conversation Flow

1. Maya introduces herself as calling from Kapture Finance.
2. Maya confirms whether she is speaking with Rahul Sharma.
3. Maya asks for a four-digit verification code.
4. Maya calls `verify_customer`.
5. Financial information is disclosed only if verification succeeds.
6. Maya explains the overdue EMI.
7. Maya identifies the customer's payment intent.
8. If the customer agrees to pay, Maya records a promise-to-pay.
9. If requested, Maya generates a payment link.
10. Maya closes the conversation professionally.

---

## Privacy and Authentication

The most important guardrail in the system is:

**No loan, EMI, overdue amount, debt, or payment information is disclosed before successful customer verification.**

The assistant does not treat a simple statement such as "I am Rahul" as sufficient authentication.

The `verify_customer` backend tool must return:

```json
{
  "verified": true
}
```

before Maya is allowed to enter the collections state.

If verification fails twice, the conversation ends without disclosing financial information.

---

## Tools

### 1. verify_customer

Verifies the customer's identity.

Endpoint:

```text
POST /verify-customer
```

Example request:

```json
{
  "customer_name": "Rahul Sharma",
  "verification_code": "1234"
}
```

Example response:

```json
{
  "verified": true,
  "customer_id": "KF001",
  "message": "Customer verified successfully"
}
```

---

### 2. log_promise_to_pay

Records the customer's payment commitment.

Endpoint:

```text
POST /log-promise-to-pay
```

Example request:

```json
{
  "customer_id": "KF001",
  "amount": 8499,
  "payment_date": "2026-08-16"
}
```

Example response:

```json
{
  "success": true,
  "customer_id": "KF001",
  "amount": 8499,
  "payment_date": "2026-08-16",
  "message": "Promise to pay recorded successfully"
}
```

---

### 3. send_payment_link

Generates a mock payment link for the verified customer.

Endpoint:

```text
POST /send-payment-link
```

Example request:

```json
{
  "customer_id": "KF001",
  "amount": 8499
}
```

Example response:

```json
{
  "success": true,
  "customer_id": "KF001",
  "amount": 8499,
  "payment_link": "https://pay.kapture-demo.com/KF001",
  "message": "Payment link generated successfully"
}
```

This is a mock payment-link generator used only for the assignment demo.

---

## Edge Cases Handled

The assistant includes conversation handling for:

* Failed customer verification
* Wrong person
* Already paid
* Financial hardship
* Cannot pay
* Payment dispute
* Callback request
* Do-not-call request
* Hostile or abusive customer
* Human assistance request

The agent avoids threats, harassment, false legal claims, and unnecessary payment pressure.

---

## Guardrails

Maya must never:

* Reveal debt information before verification
* Ask for OTPs
* Ask for passwords
* Ask for CVV
* Ask for card PIN
* Ask for banking passwords
* Threaten arrest or police action
* Invent penalties or legal consequences
* Claim a tool action succeeded before receiving a successful tool response

---

## Project Structure

```text
kapture-voicebot/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## Local Setup

Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the backend:

```bash
cd backend
python -m uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Public Webhook Setup

During local development, ngrok is used to expose the FastAPI backend to Vapi.

Example:

```bash
ngrok http 8000
```

The resulting HTTPS URL is configured as the base URL for the Vapi API Request tools.

---

## Demo Flow

### Successful Promise-to-Pay Flow

Customer confirms identity
→ enters verification code
→ `verify_customer` succeeds
→ Maya discloses overdue EMI
→ customer agrees to pay
→ `log_promise_to_pay` succeeds
→ customer requests payment link
→ `send_payment_link` succeeds
→ Maya closes the call

### Edge Case Flow

A separate test demonstrates failed verification or another edge case such as already-paid, dispute, or wrong-person handling.

---

## Testing Completed

The following flows were tested:

* Successful customer verification
* Failed verification
* Successful promise-to-pay
* Payment-link generation
* Already-paid handling
* Hardship / cannot-pay handling
* Dispute handling
* Do-not-call behavior

---

## What Broke and How It Was Debugged

During development:

* Local FastAPI endpoints were first tested using Swagger UI.
* Vapi could not directly reach localhost, so ngrok was used to expose the backend.
* The Vapi browser tool tester initially hit CORS-related network errors.
* CORS middleware was added to the FastAPI backend.
* Tool request and response schemas were validated independently before attaching them to Maya.
* Voice currency pronunciation was inconsistent, but the backend numeric values remained correct.

Testing each layer separately helped isolate frontend, webhook, and model behavior issues.

---

## Future Improvements

With more time, I would add:

* Real SMS or WhatsApp payment-link delivery
* Persistent database storage
* A dedicated call-disposition tool
* Human-agent escalation
* Callback scheduling
* Better multilingual English/Hindi handling
* Production authentication instead of demo verification codes
* Structured call analytics
* Automated conversation evaluation
* Secure API authentication
* Rate limiting and audit logging

---

## Notes

This implementation is intentionally lightweight and demo-focused.

The backend endpoints are mocked for the assignment and are not connected to a real lending or payment system.
