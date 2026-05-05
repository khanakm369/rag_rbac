from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import bcrypt
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# =========================
# ENV + MongoDB Setup
# =========================
load_dotenv()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"

client = MongoClient(MONGO_URI)
db = client["rag_userdata"]

users_collection = db["tblusers"]
roles_collection = db["tblroles"]

# =========================
# Models (JSON Input)
# =========================
class SignupRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

# =========================
# OAuth2 (Bearer Token)
# =========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# =========================
# JWT Helpers
# =========================
def create_access_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return payload

# =========================
# Home
# =========================
@app.get("/")
def home():
    return {"message": "FastAPI + MongoDB + JWT 🚀"}

# =========================
# Init Roles (Run once)
# =========================

@app.get("/roles")
def get_roles():
    roles = [r["role_name"] for r in roles_collection.find()]
    return {"roles": roles}


@app.get("/init-roles")
def init_roles():
    roles = ["Finance", "HR", "Engineering", "Marketing", "C-Level"]
    for role in roles:
        if not roles_collection.find_one({"role_name": role}):
            roles_collection.insert_one({"role_name": role})
    return {"message": "Roles initialized"}

# =========================
# Signup (JSON)
# =========================
@app.post("/signin")
def signin(data: LoginRequest):
    # 1. Find user in DB
    user = users_collection.find_one({"username": data.username})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 2. Verify password
 #   if not bcrypt.checkpw(data.password.encode(), user["password"]):
  #      raise HTTPException(status_code=401, detail="Invalid username or password")

    # 3. Create token
    token = create_access_token({
        "username": user["username"],
        "role": user["role"]
    })

    # 4. Return token
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================
# Protected Route
# =========================
@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return {
        "message": f"Welcome {user['username']}",
        "role": user["role"]
    }

# =========================
# Role-based Example
# =========================
@app.get("/admin")
def admin_only(user=Depends(get_current_user)):
    if user["role"] != "C-Level":
        raise HTTPException(status_code=403, detail="Access denied")
    return {"message": "Welcome Admin 🎯"}


@app.post("/token")
def login(data: LoginRequest):
    user = users_collection.find_one({"username": data.username})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # ✅ Make sure password is hashed in DB
    if not bcrypt.checkpw(data.password.encode(), user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "username": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

