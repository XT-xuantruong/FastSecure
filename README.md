# FastAPI API Key Authentication & Nginx Reverse Proxy

## 1. Giới thiệu

Hướng dẫn này giúp bạn triển khai **FastAPI** với **API Key** để bảo vệ API, kết hợp với **Nginx** làm reverse proxy.

## 2. Cài đặt FastAPI

Cài đặt **FastAPI** và **Uvicorn**:

```bash
pip install fastapi uvicorn
```

## 3. Tạo API với API Key

Tạo file `main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

# API Keys hợp lệ
API_KEYS = {"my-secret-key", "another-key"}

# Header chứa API Key
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="API Key không hợp lệ")
    return api_key

@app.get("/")
def home():
    return {"message": "API chạy thành công"}

@app.get("/protected")
def protected_route(api_key: str = Depends(verify_api_key)):
    return {"message": "Bạn đã truy cập API bảo mật"}
```

Chạy API trên mạng LAN:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 4. Cài đặt Nginx

Cài đặt Nginx:

```bash
sudo apt update
sudo apt install nginx -y
```

Kiểm tra trạng thái:

```bash
sudo systemctl status nginx
```

## 5. Cấu hình Nginx làm Reverse Proxy

Tạo file cấu hình Nginx:

```bash
sudo nano /etc/nginx/sites-available/fastapi
```

Thêm nội dung:

```nginx
server {
    listen 80;
    server_name 192.168.1.100;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /protected {
        proxy_pass http://127.0.0.1:8000/protected;
        proxy_set_header X-API-KEY "my-secret-key";
    }
}
```

Lưu lại (Ctrl + X → Y → Enter) và kích hoạt cấu hình:

```bash
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. Kiểm tra API

Truy cập API mở:

```bash
curl http://192.168.1.100/
```

Truy cập API bảo mật (qua FastAPI):

```bash
curl -H "X-API-KEY: my-secret-key" http://192.168.1.100/protected
```

Truy cập API bảo mật (qua Nginx - tự động chèn API Key):

```bash
curl http://192.168.1.100/protected
```

## 7. Giới hạn IP truy cập API

Chỉnh sửa file `/etc/nginx/sites-available/fastapi`:

```nginx
location /protected {
    allow 192.168.1.50;
    allow 192.168.1.60;
    deny all;
    proxy_pass http://127.0.0.1:8000/protected;
    proxy_set_header X-API-KEY "my-secret-key";
}
```

Lưu lại và restart Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## 8. Bảo mật nâng cao (Ẩn API Key)

Cài đặt `python-dotenv`:

```bash
pip install python-dotenv
```

Tạo file `.env`:

```ini
API_KEY=my-secret-key
```

Cập nhật `main.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEYS = {os.getenv("API_KEY")}
```

## 9. Tóm tắt các bước

| Bước | Mô tả                               |
| ---- | ----------------------------------- |
| 1    | Cài đặt FastAPI và Uvicorn          |
| 2    | Tạo API có xác thực bằng API Key    |
| 3    | Chạy FastAPI trên IP LAN            |
| 4    | Cài đặt Nginx                       |
| 5    | Cấu hình Nginx làm reverse proxy    |
| 6    | Kiểm tra API qua Nginx              |
| 7    | (Tùy chọn) Giới hạn IP truy cập API |
| 8    | (Tùy chọn) Ẩn API Key trong `.env`  |
