# Hệ thống gợi ý xe sử dụng Vector Database:

Bước 1: Cài đặt Qdrant:

```
docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant

```

Bước 2: Cài đặt môi trường:

Tốt nhất ta nên sử dụng môi trường ảo của conda hoặc python-venv

```
pip install -r requirements.txt
```

Tạo một file môi trường như sau:

```
QDRANT_HOST=localhost
QDRANT_PORT=6333

QDRANT_CLOUD_HOST=
QDRANT_CLOUD_API_KEY=
```

Nếu bạn sử dụng Qdrant Cloud, hãy thêm thông tin vào.

Bước 3:
Thêm dữ liệu vào các bộ sưu tập:

```
python test_add_car_to_db.py

python test_add_user.py
```

Bước 4: Sử dụng hệ thống gợi ý qua FastAPI:

```
uvicorn test_with_user_info:app --reload
```
