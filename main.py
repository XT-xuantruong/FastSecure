from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Định nghĩa API Key Header
api_key_header = APIKeyHeader(name=os.getenv('API_KEY_NAME'), auto_error=True)

def verify_ip(request: Request):
    client_ip = request.client.host # Lấy IP của client
    if client_ip not in os.getenv('ALLOWED_IPS'):
        raise HTTPException(status_code=403, detail="IP không được phép truy cập")
    
# Hàm kiểm tra API Key
def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv('API_KEY'):
        raise HTTPException(status_code=403, detail="API Key không hợp lệ")
    return api_key

@app.get("/secure-data")
async def secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "Truy cập thành công!"}

@app.get("/secure-access")
async def secure_access(request: Request, api_key: str = Depends(verify_api_key)):
    verify_ip(request)  # Kiểm tra IP hợp lệ
    return {"message": "Truy cập hợp lệ!"}
