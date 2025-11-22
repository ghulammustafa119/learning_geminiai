

from fastapi import FastAPI, HTTPException

app = FastAPI()

# Dummy database for users
users = {
    "ali": {"pin": 1111, "balance": 10000},
    "ahmed": {"pin": 2222, "balance": 8000},
    "mustafa": {"pin": 3333, "balance": 15000},
}


# -----------------------------
#   AUTHENTICATE ENDPOINT
# -----------------------------
@app.get("/authenticate")
async def authenticate(name: str, pin_number: int):
    name = name.lower()

    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if users[name]["pin"] != pin_number:
        raise HTTPException(status_code=401, detail="Incorrect PIN")

    return {
        "message": "Authentication successful",
        "name": name,
        "bank_balance": users[name]["balance"]
    }


# -----------------------------
#   BANK TRANSFER ENDPOINT
# -----------------------------
@app.post("/bank-transfer")
async def bank_transfer(sender_name: str, pin_number: int, recipient_name: str, amount: int):
    sender_name = sender_name.lower()
    recipient_name = recipient_name.lower()

    # Check sender exists
    if sender_name not in users:
        raise HTTPException(status_code=404, detail="Sender does not exist")

    # Check sender PIN
    if users[sender_name]["pin"] != pin_number:
        raise HTTPException(status_code=401, detail="Incorrect PIN for sender")

    # Check recipient exists
    if recipient_name not in users:
        raise HTTPException(status_code=404, detail="Recipient does not exist")

    # Check enough balance
    if users[sender_name]["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Transfer logic
    users[sender_name]["balance"] -= amount
    users[recipient_name]["balance"] += amount

    return {
        "message": "Transfer successful",
        "sender_balance": users[sender_name]["balance"],
        "recipient_balance": users[recipient_name]["balance"]
    }

