from fastapi import FastAPI, HTTPException
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/home")
def readroot():
    return {"message":"FastAPI is up and running!"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer.")
    return {
        "message":"user_details",
        "id":user_id
    }