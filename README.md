# Dự án TAN HOA Admin Portal API with FastAPI Python Framework Python version 3.11.3

## 🚀 Dự án được triển khai bằng lập trình hướng đối tượng OOP và mô hình MVC Pattern

## 🚀 Cấu trúc thư mục dự án

```bash
📦TanHoa_AdminPortal_backend
|── 📁logs
|── uploads
|── 📁src
|   |── 📁dto
|   |── 📁ai_module
|   |── 📁constants
|   |── 📁database
|   |── 📁controllers
|   |── 📁error
|   |── 📁jobs
|   |── 📁logs
|   |── 📁models
|   |── 📁repository
|   |── 📁routes
|   |── 📁tests
|   |── 📁utils
|   |── 📝main.py
|── 📁testing
|── 📁upload
|── 📝.config
|── 📝.editorconfig
|── ⚙️.env
|── 🗃️.gitignore
|── 🗃️.gitattributes
|── 📥README.md
|── 📥TEAM-WORK.md
|── 📥requirements.txt
```

## 📌 Ghi chú khái quát cấu trúc thư mục dự án

- 📁 'uploads' Chứa các file của server
- 📁 'dto' Chứa các hàm xử lý việc Request và Respone của một API
- 📁 'ai_module' Chứa các hàm xử lý việc tương tác với AI Moule
- 📁 'tests' Chứa các hàm xử lý việc test case API
- 📁 'database' Chứa các file xử lý việc kết nối tới Database
- 📁 'jobs' Chứa các hàm xử lý chạy ngầm trong hệ thống API
- 📁 'logs' Chứa các logs của hệ thống API
- 📁 'constants' Chứa các hằng số không thay đổi
- 📁 'routes' Chứa các route, endpoint gọi API
- 📁 'controllers' Điều luồng giữa API và "Cores", xử lý các tác vụ phức tạp trước khi trả về API
- 📁 'env' Chứa các object, biến môi trường, enum, cấu hình toàn cục
- 📁 'error' Định nghĩa các hàm, class xử lý lỗi, exception, logging error
- 📁 'models' Định nghĩa các model và schema dữ liệu (ORM hoặc đối tượng dữ liệu)
- 📁 'schedule jobs' Định nghĩa các job chạy định kỳ, cron jobs (ví dụ gửi mail, cleanup, sync dữ liệu)
- 📁 'repository' Định nghĩa các câu query để truy vấn và tương tác với Database
- 📁 'utils' Các hàm tiện ích dùng chung, helpers
- 📝 .gitignore sẽ có tác dụng loại bỏ các file không được phép đẩy lên github server

## 💻 Công nghệ dự kiến sẽ sử dụng trong dự án

`Python`, `JSON Web Token`, `FastAPI` `OpenAI`, `MongoDB`, `Motor`, `Bcrypt`

## 🚀 Khởi chạy dự án:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn src.main:app --reload --port 9000
```

- Để thoát chế độ virtual environment (venv) trong Python

```bash
deactivate
```

## Create user root MongoDB

- Muốn cấp quyền root thì phải cấp trên collection admin

```js
db.createUser({
  user: "<username>",
  pwd: "<password>",
  roles: [{ role: "root", db: "admin" }],
});
```

### Môi trường production để check SSL chạy trực tiếp file

```bash
python -m src.main
```

### Chạy dự án với Docker hub

1. RUN Dockerfile:

```bash
docker build -t tanhoa-admin-portal:0 .
```

```bash
docker build -t <tên_image>[:tag] <đường_dẫn_build_context>
```

- Với `fastapi-app`: name Docker Image

2. RUN Docker container:

```bash
docker run -it --rm -p 9000:9000 --env-file .env tanhoa-admin-portal:0
```

## Ghi chú

```bash
ACCESS_TOKEN_EXPIRED_IN= # 1 ngày = 24 × 60 x 60
REFRESH_TOKEN_EXPIRED_IN= # 30 ngày = 30 x 24 × 60 x 30
```
