from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
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

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"

client = MongoClient(MONGO_URI)
db = client["rag_userdata"]

users_collection = db["tblusers"]
roles_collection = db["tblroles"]

# =========================
# CORS FIX (IMPORTANT)
# =========================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # ✅ NOT "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Models
# =========================
class SignupRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

# =========================
# OAuth2
# =========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# =========================
# JWT Helpers
# =========================
def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# =========================
# Home
# =========================
@app.get("/")
def home():
    return {"message": "API Running 🚀"}

# =========================
# Roles
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
# Signup (hash password)
# =========================
@app.post("/signup")
def signup(data: SignupRequest):
    role = data.role.strip()

    if not roles_collection.find_one({"role_name": role}):
        raise HTTPException(status_code=400, detail="Invalid role")

    if users_collection.find_one({"username": data.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    # 🔐 HASH PASSWORD
    hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

    users_collection.insert_one({
        "username": data.username,
        "password": hashed_password,  # stored as bytes
        "role": role
    })

    return {"message": "User created successfully"}

# =========================
# Login (JWT)
# =========================
@app.post("/token")
def login(data: LoginRequest):
    user = users_collection.find_one({"username": data.username})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # ✅ SAFE PASSWORD CHECK
    stored_password = user["password"]

    # Handle both cases (old plain text + new hashed)
    if isinstance(stored_password, str):
        if data.password != stored_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    else:
        if not bcrypt.checkpw(data.password.encode(), stored_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "username": user["username"],
        "role": user["role"]
    })

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
# Role-based Route
# =========================
@app.get("/admin")
def admin(user=Depends(get_current_user)):
    if user["role"] != "C-Level":
        raise HTTPException(status_code=403, detail="Access denied")
    return {"message": "Welcome Admin 🎯"}