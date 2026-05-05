from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

# Correcting the argument to 'tokenUrl' (case-sensitive)
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(token: str = Depends(oauth2_schema)):
    # If the token isn't what we "decided" in the login route, kick them out
    if token != "secret-static-token-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"user_id": 1, "username": "admin", "role": "superuser"}