from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VerifyCustomerRequest(BaseModel):
    customer_name: str
    verification_code: str


class PromiseToPayRequest(BaseModel):
    customer_id: str
    amount: int
    payment_date: str


class PaymentLinkRequest(BaseModel):
    customer_id: str
    amount: float


@app.get("/")
def home():
    return {
        "message": "Kapture Voicebot Backend is running"
    }


@app.post("/verify-customer")
def verify_customer(data: VerifyCustomerRequest):

    if (
        data.customer_name.lower() == "rahul sharma"
        and data.verification_code == "1234"
    ):
        return {
            "verified": True,
            "customer_id": "KF001",
            "message": "Customer verified successfully"
        }

    return {
        "verified": False,
        "message": "Customer verification failed"
    }


@app.post("/log-promise-to-pay")
def log_promise_to_pay(data: PromiseToPayRequest):

    return {
        "success": True,
        "customer_id": data.customer_id,
        "amount": data.amount,
        "payment_date": data.payment_date,
        "message": "Promise to pay recorded successfully"
    }


@app.post("/send-payment-link")
def send_payment_link(data: PaymentLinkRequest):

    payment_link = f"https://pay.kapture-demo.com/{data.customer_id}"

    return {
        "success": True,
        "customer_id": data.customer_id,
        "amount": data.amount,
        "payment_link": payment_link,
        "message": "Payment link generated successfully"
    }