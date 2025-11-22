from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

router = APIRouter(prefix="/api/users", tags=["User API"])


# ============================
# 1) Pydantic Models (Validation)
# ============================

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=1, le=120)
    country: Optional[str] = "Unknown"


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=1, le=120)
    country: Optional[str] = None


class User(BaseModel):
    id: int
    name: str
    age: int
    country: str


# ============================
# 2) Fake Database (in-memory)
# ============================

db = {
    1: {"id": 1, "name": "Ali", "age": 22, "country": "Pakistan"},
    2: {"id": 2, "name": "Sara", "age": 25, "country": "USA"},
}

next_id = 3  # next user ID


# ============================
# 3) GET Users List (Query Params)
# ============================

@router.get("/", response_model=List[User])
def user_list(page: int = 1, limit: int = 10, country: Optional[str] = None):

    user_list = list(db.values())

    # Filtering
    if country:
        user_list = [u for u in user_list if u["country"].lower() == country.lower()]

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    return user_list[start:end]


# ============================
# 4) GET User Details (Path Param)
# ============================

@router.get("/{user_id}", response_model=User)
def user_details(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return db[user_id]


# ============================
# 5) CREATE User (POST)
# ============================

@router.post("/", response_model=User, status_code=201)
def create_user(data: UserCreate):
    global next_id

    new_user = {
        "id": next_id,
        "name": data.name,
        "age": data.age,
        "country": data.country,
    }

    db[next_id] = new_user
    next_id += 1

    return new_user


# ============================
# 6) UPDATE User (PUT)
# ============================

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, data: UserUpdate):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")

    user = db[user_id]

    # Patch update (sirf wahi fields update hongi jo bheje gaye)
    if data.name is not None:
        user["name"] = data.name
    if data.age is not None:
        user["age"] = data.age
    if data.country is not None:
        user["country"] = data.country

    return user


# ============================
# 7) DELETE User (DELETE)
# ============================

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")

    del db[user_id]
    return {"message": "User deleted successfully"}


# Include Router
app.include_router(router)