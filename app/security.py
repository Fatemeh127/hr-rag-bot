from fastapi import Header, HTTPException
import os

API_KEY_ROLE_MAP = {
    os.getenv("EMPLOYEE_API_KEY"): "employee",
    os.getenv("MANAGER_API_KEY"): "manager",
    os.getenv("ADMIN_API_KEY"): "admin"
}


def get_current_role(x_api_key:str = Header(None)) -> str:
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key"
        )
    role = API_KEY_ROLE_MAP.get(x_api_key)

    if not role:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    
    return role