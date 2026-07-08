import time
import uuid
from fastapi import Request

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import jwt

from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-gygra9.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response


@app.get("/")
def home():
    return {
        "message": "Metrics API is running"
    }

class TokenRequest(BaseModel):
    token: str

with open("public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()

@app.get("/stats")
def get_stats(values: str = Query(...)):
    nums = [int(x) for x in values.split(",")]

    return {
        "email": "23f2004761@ds.study.iitm.ac.in",
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums)
    }
@app.post("/verify")
def verify_token(data: TokenRequest):
    try:
        payload = jwt.decode(
            data.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer="https://idp.exam.local",
            audience="tds-no1cqrmm.apps.exam.local",
        )

        return {
            "valid": True,
            "email": payload["email"],
            "sub": payload["sub"],
            "aud": payload["aud"],
        }

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail={"valid": False},
        )