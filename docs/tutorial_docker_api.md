# Docker + FastAPI — Mini Tutorial

این tutorial خلاصه‌ی چیزهایی است که تا اینجا **عملاً با هم انجام داده‌ایم**. هدف آن مرور سریع است، نه آموزش تئوری مفصل.

---

# Part 1 — مفاهیم پایه API

## 1. API چیست؟

**API = Application Programming Interface**

یعنی یک **راه استاندارد برای ارتباط بین دو نرم‌افزار**.

مثلاً:

```text
Python App  ───── request ─────>  Weather Service
Python App  <──── response ─────  Weather Service
```

API مشخص می‌کند:

> «اگر می‌خواهی از من اطلاعات بگیری یا کاری بخواهی، درخواستت را این‌طور بفرست و من جواب را این‌طور برمی‌گردانم.»

---

## 2. HTTP چیست؟

**HTTP = Hypertext Transfer Protocol**

پروتکلی است که request و responseهای وب/API معمولاً از طریق آن منتقل می‌شوند.

مدل ذهنی:

```text
Client
   │
   │ HTTP Request
   ▼
Server / API
   │
   │ HTTP Response
   ▼
Client
```

---

## 3. REST API چیست؟

**REST = Representational State Transfer**

REST یک **سبک طراحی API** است.

معمولاً resourceها را با URL مشخص می‌کنیم و از HTTP methods استفاده می‌کنیم:

```text
GET    /users
GET    /users/123
POST   /users
PUT    /users/123
DELETE /users/123
```

معنی ساده:

| Method | معنی                |
| ------ | ------------------- |
| GET    | چیزی را بگیر        |
| POST   | چیزی ایجاد/ارسال کن |
| PUT    | چیزی را تغییر بده   |
| DELETE | چیزی را حذف کن      |

مثلاً:

```text
GET /users/123
```

یعنی:

> اطلاعات user شماره 123 را بده.

**REST API = APIای که طبق اصول REST طراحی شده است.**

---

## 4. FastAPI چیست؟

**FastAPI یک Python Framework برای ساخت API است.**

مثلاً:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello"}
```

حالا API ما endpoint زیر را دارد:

```text
GET /hello
```

پس:

> **FastAPI خودش API نیست؛ ابزاری برای ساخت API است.**

و می‌توانیم با FastAPI یک REST API بسازیم.

---

## 5. OpenAPI چیست؟

**OpenAPI یک Specification برای توصیف API است.**

یعنی مشخص می‌کند:

* چه endpointهایی داریم؟
* چه methodهایی دارند؟
* چه parametersهایی می‌گیرند؟
* request body چیست؟
* response چیست؟
* چه خطاهایی ممکن است رخ دهد؟

مثلاً:

```text
GET /users/{id}

Input:
    id: integer

Response:
    name: string
    age: integer
```

OpenAPI را می‌توان مثل **نقشه/شناسنامه‌ی API** در نظر گرفت.

---

## 6. Swagger UI چیست؟

FastAPI به‌صورت خودکار documentation تعاملی می‌سازد.

در:

```text
http://localhost:8000/docs
```

می‌توانی endpointها را ببینی و مستقیماً test کنی.

Swagger UI از OpenAPI specification استفاده می‌کند.

پس:

| اصطلاح     | چیست؟                   | نقش                     |
| ---------- | ----------------------- | ----------------------- |
| API        | رابط ارتباط نرم‌افزارها | ارتباط                  |
| REST API   | سبک طراحی API           | نحوه طراحی              |
| FastAPI    | Python framework        | ساخت API                |
| HTTP       | پروتکل ارتباطی          | انتقال request/response |
| OpenAPI    | استاندارد توصیف API     | specification           |
| Swagger UI | UI برای API             | مشاهده و تست            |

### جمله‌های یک‌خطی برای مرور

> **API:** راه ارتباط دو نرم‌افزار.

> **REST API:** APIای که طبق اصول REST طراحی شده.

> **FastAPI:** ابزار Python برای ساخت API.

> **OpenAPI:** استانداردی برای توصیف API.

> **Swagger UI:** صفحه‌ای برای مشاهده و تست API.

این مفاهیم در مسیر ما به این زنجیره وصل می‌شوند:

```text
Python → FastAPI → REST API → HTTP → Docker
```

یعنی با **FastAPI** یک API می‌سازی، این API از طریق **HTTP** قابل دسترسی است و بعد application را داخل **Docker** اجرا می‌کنی.

---

# Part 2 — Docker Basics

## 7. Docker چیست؟

Docker به ما اجازه می‌دهد application و dependencies آن را داخل یک **container** اجرا کنیم.

سه مفهوم اصلی:

```text
Image      → template/package برای ساخت container
Container  → instance در حال اجرای image
Dockerfile → دستورالعمل ساخت image
```

---

## 8. اجرای یک container آماده

ما ابتدا Nginx را اجرا کردیم:

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

معنی:

```text
docker run       → یک container از یک image بساز و اجرا کن
-d               → detached؛ در background اجرا شود
--name my-nginx  → اسم container
-p 8080:80       → port mapping
nginx            → image مورد استفاده
```

`-p 8080:80` یعنی:

```text
Host port 8080 → Container port 80
```

بنابراین:

```text
Browser
   ↓
localhost:8080
   ↓
Docker
   ↓
container:80
   ↓
Nginx
```

---

## 9. دستورات مهم Docker

### دیدن containerهای در حال اجرا

```bash
docker ps
```

### دیدن همه containerها

```bash
docker ps -a
```

`-a` یعنی all؛ شامل stopped containerها هم می‌شود.

### توقف

```bash
docker stop my-nginx
```

### اجرای دوباره

```bash
docker start my-nginx
```

### حذف

```bash
docker rm my-nginx
```

اگر در حال اجرا باشد:

```bash
docker rm -f my-nginx
```

`-f` یعنی force.

---

## 10. Docker Logs

```bash
docker logs my-nginx
```

برای دیدن output/logهای process اصلی container.

---

## 11. ورود به داخل container

```bash
docker exec -it my-nginx bash
```

معنی:

```text
docker exec → اجرای command داخل container در حال اجرا
-i           → interactive
-t           → terminal / TTY
my-nginx     → container هدف
bash         → shell
```

مثلاً:

```bash
ls
```

و برای خروج:

```bash
exit
```

تفاوت مهم:

```text
docker logs → دیدن output برنامه
docker exec → اجرای command داخل container
```

---

# Part 3 — ساخت Docker Image

## 12. ساخت یک Python application

ساختار:

```text
~/n8n-learning/
└── docker-python/
    ├── app.py
    └── Dockerfile
```

`app.py`:

```python
print("Hello from my Dockerized Python application!")
```

`Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

### معنی Dockerfile

```dockerfile
FROM python:3.12-slim
```

image پایه.

```dockerfile
WORKDIR /app
```

working directory داخل container.

```dockerfile
COPY app.py .
```

کپی کردن `app.py` به working directory.

```dockerfile
CMD ["python", "app.py"]
```

command اصلی هنگام اجرای container.

---

## 13. Build

```bash
docker build -t my-python-app .
```

معنی:

```text
docker build → ساخت image
-t            → تعیین tag/name
my-python-app → نام image
.             → build context؛ directory فعلی
```

## Run

```bash
docker run --name my-python-container my-python-app
```

اگر application تمام شود، container هم متوقف می‌شود.

مثلاً:

```text
Exited (0)
```

یعنی process با موفقیت تمام شده، نه اینکه الزاماً error رخ داده باشد.

---

# Part 4 — FastAPI داخل Docker

## 14. ساختار پروژه

```text
fastapi-basic/
├── main.py
├── requirements.txt
└── Dockerfile
```

### requirements.txt

```text
fastapi[standard]
```

یعنی FastAPI و dependencies استاندارد لازم برای اجرای آن.

---

## 15. FastAPI application

```python
from fastapi import FastAPI

app = FastAPI()
```

`app` شیء اصلی FastAPI application است.

---

## 16. اولین endpoint

```python
@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI"}
```

### معنی

```python
@app.get("/hello")
```

یعنی:

> وقتی HTTP GET به `/hello` آمد، function زیر را اجرا کن.

```python
def hello():
```

function مربوط به request.

```python
return {"message": "Hello from FastAPI"}
```

FastAPI این dictionary را به JSON response تبدیل می‌کند.

---

# Part 5 — Dockerizing FastAPI

## 17. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

### نکات مهم

```dockerfile
RUN
```

command را هنگام **build شدن image** اجرا می‌کند.

بنابراین:

```dockerfile
RUN pip install ...
```

dependencyها داخل image نصب می‌شوند.

```dockerfile
CMD
```

command پیش‌فرض هنگام اجرای container است.

---

## 18. Build و Run

```bash
docker build -t fastapi-basic .
```

سپس:

```bash
docker run --name fastapi-basic-container -p 8000:8000 fastapi-basic
```

معنی:

```text
--name fastapi-basic-container
```

نام container.

```text
-p 8000:8000
```

یعنی:

```text
Host port 8000 → Container port 8000
```

در نتیجه:

```text
localhost:8000
      ↓
Docker container:8000
      ↓
FastAPI
```

---

# Part 6 — curl و HTTP Requests

## 19. GET ساده

```bash
curl http://localhost:8000/hello
```

`curl` یک command-line HTTP client است.

---

## 20. نمایش HTTP headers

```bash
curl -i http://localhost:8000/hello
```

`-i` یعنی response headers را هم نمایش بده.

مثلاً:

```text
HTTP/1.1 200 OK
content-type: application/json
```

---

# Part 7 — POST + JSON + Pydantic

## 21. Pydantic چیست؟

**Pydantic یک Python library برای validate و structure کردن data است.**

مثلاً:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

یعنی انتظار داریم:

```json
{
  "name": "Zahra",
  "age": 35
}
```

Pydantic بررسی می‌کند که داده با model سازگار باشد.

### مدل ذهنی

```text
Client
  │
  │ JSON
  ▼
FastAPI
  │
  ▼
Pydantic
  │
  │ validation
  ▼
Python object
  │
  ▼
Your function
```

### تفاوت مهم

**Type hint:**

```python
age: int
```

می‌گوید چه typeای انتظار داریم.

**Pydantic model:**

```python
class User(BaseModel):
    age: int
```

ساختار داده را تعریف و validation می‌کند.

**FastAPI** از این type information و Pydantic برای validation و API schema استفاده می‌کند.

---

## 22. POST endpoint

```python
class UserRequest(BaseModel):
    name: str
    age: int


@app.post("/users")
def create_user(user: UserRequest):
    return {
        "message": f"Hello {user.name}!",
        "age": user.age
    }
```

```python
@app.post("/users")
```

یعنی این endpoint با HTTP POST روی `/users` کار می‌کند.

```python
user: UserRequest
```

یعنی request body باید مطابق `UserRequest` باشد.

---

## 23. ارسال JSON با curl

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Zahra","age":35}'
```

پارامترهای مهم:

```text
-X POST
```

`-X` = تعیین HTTP method.

```text
-H "Content-Type: application/json"
```

`-H` = HTTP header.

اینجا به server می‌گوییم body ما JSON است.

```text
-d '{"name":"Zahra","age":35}'
```

`-d` = data؛ داده‌ای که همراه request ارسال می‌کنیم.

---

# Part 8 — Validation

اگر بفرستیم:

```json
{
  "name": "Zahra",
  "age": "Taheri"
}
```

FastAPI/Pydantic می‌گوید:

```text
422 Unprocessable Entity
```

چون:

```python
age: int
```

ولی `"Taheri"` integer نیست.

---

# Part 9 — Type Hints و Validation

این:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

هم validation دارد.

مثلاً:

```bash
curl http://localhost:8000/users/42
```

موفق است.

ولی:

```bash
curl http://localhost:8000/users/zahra
```

→ `422`

چرا؟

چون FastAPI از:

```python
user_id: int
```

می‌فهمد که `user_id` باید integer باشد و validation انجام می‌دهد.

نکته مهم:

> لازم نیست حتماً parameter داخل `BaseModel` باشد تا FastAPI از type hint برای validation استفاده کند.

---

# Part 10 — Path Parameter

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

اینجا:

```text
/users/42
```

`42` یک **Path Parameter** است.

```text
/users/{user_id}
```

مسیر endpoint است و `{user_id}` جای مقدار واقعی را مشخص می‌کند.

---

# Part 11 — Query Parameter

```python
@app.get("/search")
def search_users(name: str, age: int | None = None):
    return {
        "name": name,
        "age": age
    }
```

مثال:

```text
/search?name=Zahra&age=42
```

دارای دو Query Parameter است:

```text
name=Zahra
age=42
```

```python
name: str
```

یعنی `name` required است.

```python
age: int | None = None
```

یعنی `age` optional است.

مثلاً:

```bash
curl "http://localhost:8000/search?name=Zahra"
```

معتبر است.

اما:

```bash
curl "http://localhost:8000/search"
```

→ `422`

چون `name` required است.

---

# Part 12 — سه نوع ورودی مهم API

این سه مورد را حتماً در ذهن نگه دار:

### 1. Path Parameter

```text
/users/42
```

```python
user_id: int
```

### 2. Query Parameter

```text
/search?name=Zahra&age=42
```

```python
name: str
age: int | None = None
```

### 3. Request Body

```json
{
  "name": "Zahra",
  "age": 42
}
```

```python
class UserRequest(BaseModel):
    name: str
    age: int
```

این سه مورد برای کار بعدی ما با **n8n و LLM APIs** بسیار مهم‌اند.

---

# Part 13 — HTTP Status Codes

چند status code مهم که تا الان دیدی:

```text
200 OK
```

درخواست موفق.

```text
404 Not Found
```

route وجود ندارد.

مثلاً:

```text
/search/Zahra/42
```

در حالی که فقط `/search` تعریف شده است.

```text
422 Unprocessable Entity
```

route وجود دارد، اما داده‌ی ورودی مطابق type/schema مورد انتظار نیست.

مثلاً:

```text
age=Taheri
```

---

# Part 14 — AI-like Endpoint

برای اینکه از تمرین ساده API به سمت **AI service** حرکت کنیم، این endpoint را ساختیم:

```python
class AnalyzeRequest(BaseModel):
    text: str


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    return {
        "text": request.text,
        "length": len(request.text),
        "message": "Text received successfully!"
    }
```

### معنی

```python
class AnalyzeRequest(BaseModel):
    text: str
```

request body باید شامل `text` باشد و `text` باید string باشد.

```python
@app.post("/analyze")
```

یعنی:

> HTTP POST روی `/analyze` → function زیر را اجرا کن.

```python
request: AnalyzeRequest
```

یعنی body را مطابق `AnalyzeRequest` دریافت و validate کن.

---

## تست

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Docker makes AI deployment easier."}'
```

نتیجه:

```json
{
  "text": "Docker makes AI deployment easier.",
  "length": 34,
  "message": "Text received successfully!"
}
```

این endpoint هنوز LLM واقعی ندارد؛ فقط **ساختار AI service** را شبیه‌سازی می‌کند.

مدل ذهنی:

```text
Client / n8n
      ↓
POST /analyze
      ↓
FastAPI
      ↓
AI logic
      ↓
JSON response
```

بعداً `AI logic` را با LLM واقعی جایگزین می‌کنیم.

---

# Part 15 — Sandbox

**Sandbox = محیط آزمایشی / ایزوله**

Sandbox یک تکنولوژی خاص نیست؛ یک **مفهوم** است.

یعنی:

> محیطی جدا و کم‌خطر که بتوانی چیزی را آزمایش کنی، خراب کنی و دوباره بسازی، بدون اینکه پروژه اصلی آسیب ببیند.

در آموزش فعلی ما:

```text
Learning Sandbox
│
├── Docker
├── FastAPI
├── HTTP
├── JSON
└── بعداً Docker Compose
```

پروژه‌ی کوچک:

```text
fastapi-basic/
├── main.py
├── requirements.txt
└── Dockerfile
```

Sandbox ماست.

اگر container خراب شود یا حذفش کنیم، مهم نیست؛ پروژه واقعی دست‌نخورده می‌ماند.

### Docker ≠ Sandbox

```text
Docker = containerization technology
Sandbox = concept of an isolated/testing environment
```

Docker **می‌تواند** برای ساخت یک sandbox استفاده شود، اما Docker ذاتاً مترادف sandbox نیست.

---

# Part 16 — Environmentهای مختلف

ممکن است این اصطلاحات را ببینی:

```text
Development environment → محیط توسعه
Testing environment     → محیط تست
Staging environment     → محیط شبیه production برای تست نهایی
Production environment  → محیط واقعی
Sandbox                 → محیط جدا و کم‌خطر برای آزمایش
```

در مسیر ما:

```text
Docker/FastAPI Sandbox
          ↓
        n8n
          ↓
   LLM Systems Lab
```

یعنی ابتدا ابزارها را در محیط کوچک یاد می‌گیریم، سپس همان مهارت‌ها را روی پروژه واقعی اعمال می‌کنیم.

---

# Part 17 — مدل ذهنی کلی تا اینجا

```text
                    API
                     │
          ┌──────────┴──────────┐
          │                     │
      REST API              سایر APIها
          │
       با HTTP
          │
          ▼
       FastAPI
          │
    Python Framework
          │
          ▼
      API می‌سازد
          │
          ▼
       OpenAPI
          │
     API را توصیف می‌کند
```

و برای پروژه‌ی خودمان:

```text
                 Docker
                   │
                   ▼
             FastAPI app
                   │
          ┌────────┼────────┐
          │        │        │
       Path     Query     Body
       param    param     JSON
          │        │        │
          └────────┼────────┘
                   ▼
                Pydantic
                   │
               validation
                   │
                   ▼
              AI / LLM logic
                   │
                   ▼
              JSON response
```

---

# Part 18 — مهم‌ترین زنجیره برای AI Engineering

فعلاً لازم نیست FastAPI را عمیق‌تر از این یاد بگیری.

چیزی که باید در ذهنت تثبیت شود:

```text
Client / n8n
      │
      │ HTTP + JSON
      ▼
   FastAPI
      │
      │ Pydantic validation
      ▼
 AI / LLM service
      │
      ▼
 JSON result
      │
      ▼
 n8n / Client
```

و کل application:

```text
FastAPI
   ↓
Docker image
   ↓
Docker container
   ↓
HTTP endpoint
```

---

# 🧠 One-minute revision

اگر فقط یک دقیقه وقت داشتی:

```text
API        = راه ارتباط نرم‌افزارها
HTTP       = پروتکل ارتباط
REST       = سبک طراحی API
FastAPI    = Python framework برای ساخت API
Pydantic   = تعریف/validation داده
OpenAPI    = specification برای توصیف API
Swagger UI  = UI برای مشاهده و تست API
Docker     = package/run کردن application در container
Sandbox    = محیط آزمایشی جدا
```

و:

```text
Path      → /users/42
Query     → /search?name=Zahra
Body      → {"name":"Zahra","age":42}

GET       → دریافت
POST      → ارسال/ایجاد
200       → موفق
404       → route پیدا نشد
422       → ورودی نامعتبر
```

---

# 🎯 هدف ما از اینجا

دیگر قرار نیست FastAPI را به‌صورت آکادمیک ادامه بدهیم.

فقط موارد ضروری را یاد می‌گیریم و سریع حرکت می‌کنیم:

```text
                    ✓ Docker
                      │
                    ✓ FastAPI
                      │
                    ✓ HTTP / JSON
                      │
                    ✓ Pydantic
                      │
                 [NOW]
                      │
              Environment variables
                      │
                 Docker Compose
                      │
                    n8n
                      │
                      ▼
             Real LLM Service
                      │
                      ▼
              LLM Systems Lab
                      │
                      ▼
              Agentic AI / Tools
                      │
                      ▼
                     MCP
```

هدف نهایی این نیست که بگویی:

> «من FastAPI بلدم.»

هدف این است که بتوانی با اطمینان بگویی:

> **«من می‌توانم یک AI/LLM service را با Python/FastAPI بسازم، Dockerize کنم، از طریق HTTP/JSON به آن دسترسی بدهم، آن را به n8n متصل کنم و در نهایت در یک AI workflow واقعی استفاده کنم.»**

این برای مسیر **Applied AI / AI Engineer / LLM Engineer** بسیار مهم‌تر از دانستن ده‌ها feature اضافی FastAPI است.


# Practical Completion Checklist — Docker + FastAPI

Before moving to Docker Compose and n8n, I should be able to do the following **without copying the tutorial line by line**.

## 🟢 Docker

* [ ] I can explain the difference between an **image** and a **container**.
* [ ] I can read a Dockerfile containing:

  * [ ] `FROM`
  * [ ] `WORKDIR`
  * [ ] `COPY`
  * [ ] `RUN`
  * [ ] `CMD`
* [ ] I can build an image:

  ```bash
  docker build -t my-app .
  ```
* [ ] I can run a container:

  ```bash
  docker run --name my-container my-app
  ```
* [ ] I understand why a container may show `Exited (0)`.
* [ ] I can map a port:

  ```bash
  docker run -p 8000:8000 my-app
  ```
* [ ] I can check running and stopped containers:

  ```bash
  docker ps
  docker ps -a
  ```
* [ ] I can view logs:

  ```bash
  docker logs my-container
  ```
* [ ] I can enter a running container:

  ```bash
  docker exec -it my-container bash
  ```
* [ ] I can stop, start, and remove a container:

  ```bash
  docker stop my-container
  docker start my-container
  docker rm my-container
  ```

---

## 🟢 HTTP / REST / API

* [ ] I understand the difference between **API**, **HTTP API**, and **REST API**.
* [ ] I know what these HTTP methods are generally used for:

  * [ ] `GET`
  * [ ] `POST`
  * [ ] `PUT`
  * [ ] `PATCH`
  * [ ] `DELETE`
* [ ] I understand the difference between:

  * [ ] Path parameter → `/users/42`
  * [ ] Query parameter → `/users?age=42`
  * [ ] Request body → JSON sent with `POST`
* [ ] I understand what JSON is.
* [ ] I understand the basic meaning of common status codes:

  * [ ] `200`
  * [ ] `201`
  * [ ] `400`
  * [ ] `404`
  * [ ] `422`
  * [ ] `500`
* [ ] I can send a GET request with `curl`.
* [ ] I can send a POST request with JSON using:

  ```bash
  curl -X POST ... -H "Content-Type: application/json" -d '...'
  ```

---

## 🟢 FastAPI

* [ ] I understand that **FastAPI is a Python framework for building APIs**.
* [ ] I can create a basic FastAPI application.
* [ ] I can create a `GET` endpoint.
* [ ] I can create a `POST` endpoint.
* [ ] I can use path parameters.
* [ ] I can use query parameters.
* [ ] I can define a request model with Pydantic:

  ```python
  class RequestModel(BaseModel):
      ...
  ```
* [ ] I understand that FastAPI + Pydantic automatically validate incoming data.
* [ ] I understand why incorrect input can produce `422`.
* [ ] I can run FastAPI inside Docker.
* [ ] I can access the API from outside the container.
* [ ] I know where to find the automatically generated API documentation:

  ```
  /docs
  ```

---

## 🟢 AI Engineering Connection

I should be able to explain this architecture in my own words:

```text
Python application
       ↓
    FastAPI
       ↓
   REST / HTTP
       ↓
   JSON request
       ↓
 Docker container
       ↓
AI / LLM service
```

And I should understand that the same pattern will later allow me to build:

```text
n8n
  ↓
FastAPI
  ↓
AI / LLM
  ↓
result
  ↓
n8n
  ↓
action
```

---

## 🟢 Practical Test

Without looking at the tutorial, I should be able to build a small service that:

* [ ] Has a FastAPI application.
* [ ] Has `GET /hello`.
* [ ] Has `POST /analyze`.
* [ ] Accepts JSON such as:

  ```json
  {
    "text": "Docker makes AI deployment easier."
  }
  ```
* [ ] Returns at least:

  ```json
  {
    "text": "...",
    "length": 34
  }
  ```
* [ ] Uses a Pydantic model for the request.
* [ ] Runs successfully inside Docker.
* [ ] Is accessible through:

  ```text
  http://localhost:8000
  ```
* [ ] Can be tested with both `curl` and `/docs`.

---

## 🟢 Troubleshooting Test

If something goes wrong, I should first be able to check:

```bash
docker ps
docker ps -a
docker logs <container>
```

and understand whether the problem is likely related to:

* [ ] container not running
* [ ] application error
* [ ] wrong port
* [ ] wrong URL/path
* [ ] invalid JSON
* [ ] invalid input type
* [ ] outdated Docker image after changing source code

---

## 🟡 I Understand, But Don't Need to Master Yet

* [ ] OpenAPI specification
* [ ] Swagger UI internals
* [ ] Uvicorn internals
* [ ] Advanced Pydantic features
* [ ] Advanced FastAPI dependency injection
* [ ] Async programming details
* [ ] Advanced HTTP semantics

I only need enough understanding to use them effectively in an AI application.

---

## 🔴 Not Needed Yet

I do **not** need to study these at this stage:

* [ ] Kubernetes
* [ ] Docker Swarm
* [ ] Advanced Docker networking
* [ ] Advanced FastAPI architecture
* [ ] Complex authentication systems
* [ ] Enterprise DevOps
* [ ] Advanced reverse-proxy configuration
* [ ] Microservice architecture patterns

These can wait until a real project requires them.

---

## Final Milestone

If I can complete the **Practical Test** above independently, I am ready to move on.

### Next step:

**Docker Compose → n8n → connecting n8n to my FastAPI service → real AI/LLM workflow**
