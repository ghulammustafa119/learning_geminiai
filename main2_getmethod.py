from fastapi import FastAPI, APIRouter, HTTPException
from typing import Optional

app = FastAPI()

router = APIRouter(prefix="/api/users")  
# Ab sab routes user-related isi prefix ke andar honge
# Final URLs: /api/users/...

# ============================
# 1) GET Users List (Query Params)
# ============================

@router.get("/")
def get_users(
    page: int = 1,
    limit: int = 10,
    country: Optional[str] = None
):
    """
    User list query parameters ke sath:
    - page aur limit pagination ke liye hain
    - country optional filter hai
    """

    fake_data = [
        {"id": 1, "name": "Ali", "country": "Pakistan"},
        {"id": 2, "name": "Sara", "country": "USA"},
        {"id": 3, "name": "John", "country": "Pakistan"},
        {"id": 4, "name": "Aisha", "country": "UK"},
         {"id": 5, "name": "Nayab", "country": "Pakistan"},
        {"id": 6, "name": "Anmol", "country": "USA"},
        {"id": 7, "name": "Shumaila", "country": "Pakistan"},
        {"id": 8, "name": "Mujtaba", "country": "UK"},
         {"id": 9, "name": "Mustafa", "country": "Pakistan"},
        {"id": 10, "name": "Ghulam", "country": "USA"},
        {"id": 11, "name": "Bhutto", "country": "Pakistan"},
        {"id": 12, "name": "Nayab Bhutto", "country": "UK"},
    ]

    # Country filter logic
    if country:
        fake_data = [u for u in fake_data if u["country"].lower() == country.lower()]

    # Pagination logic
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(fake_data),
        "results": fake_data[start:end]
    }


# ============================
# 2) GET User Details (Path Param)
# ============================

@router.get("/{user_id}")
def get_user_details(user_id: int):
    """
    Specific user details path parameter ke sath:
    /api/users/10
    """

    fake_data = {
        1: {"id": 1, "name": "Ali", "age": 22},
        2: {"id": 2, "name": "Sara", "age": 25},
        3: {"id": 3, "name": "John", "age": 30},
    }

    if user_id not in fake_data:
        raise HTTPException(status_code=404, detail="User not found")

    return fake_data[user_id]


# Include router
app.include_router(router)