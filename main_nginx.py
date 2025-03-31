from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI đang chạy qua Nginx"}
