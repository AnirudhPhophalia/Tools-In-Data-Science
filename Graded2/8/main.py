from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()


class ExtractRequest(BaseModel):
    text: str


class ExtractResponse(BaseModel):
    vendor: str
    amount: float
    currency: str
    date: str


@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):

    text = req.text.strip()

    if not text:
        return ExtractResponse(
            vendor="",
            amount=0.0,
            currency="USD",
            date="1970-01-01"
        )

    vendor = ""

    amount = 0.0

    currency = "USD"

    date = "1970-01-01"

    # Date
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", text)
    if m:
        date = m.group(1)

    # Currency
    m = re.search(r"\b(USD|EUR|GBP)\b", text, re.IGNORECASE)
    if m:
        currency = m.group(1).upper()

    # Amount
    m = re.search(
        r"(?:Total(?: Due)?|Amount(?: Due)?|Due)\D*([0-9]+(?:\.[0-9]+)?)",
        text,
        re.IGNORECASE,
    )

    if not m:
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)", text)

    if m:
        amount = float(m.group(1))

    # Vendor
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:
        vendor = lines[0]

    return ExtractResponse(
        vendor=vendor,
        amount=amount,
        currency=currency,
        date=date
    )