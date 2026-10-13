# Docker Compose و ارتباط سرویس‌های AI — Tutorial مرور و مصاحبه

این راهنما تمام مراحلی را که پس از آموزش Environment Variables انجام دادیم، از اولین اجرای Docker Compose تا ارتباط دو سرویس FastAPI و مدیریت خطا پوشش می‌دهد.

## 1. اجرای FastAPI با Docker Compose

هدف: مدیریت ساخت و اجرای container برنامه با یک فایل پیکربندی.

فایل `compose.yaml` در مسیر `~/n8n-learning`:

```

services:
  api:
    build: ./fastapi-basic
    container_name: fastapi-api
    ports:
      - "8000:8000"
    env_file:
      - ./fastapi-basic/.env

```

توضیح اجزای فایل:

| دستور یا کلید            | کاربرد                                            |
| ------------------------ | ------------------------------------------------- |
| `services`               | تعریف سرویس‌های برنامه                            |
| `api`                    | نام سرویس؛ بعداً برای ارتباط داخلی استفاده می‌شود |
| `build: ./fastapi-basic` | ساخت Docker image با Dockerfile داخل این مسیر     |
| `container_name`         | تعیین نام container                               |
| `ports: "8000:8000"`     | اتصال پورت ۸۰۰۰ میزبان به پورت ۸۰۰۰ container     |
| `env_file`               | خواندن environment variables از فایل مشخص‌شده     |

در نگاشت پورت، عدد سمت چپ پورت میزبان و عدد سمت راست پورت داخل container است.

### دستورات اصلی

```
docker compose up --build
```

سرویس‌ها را می‌سازد و اجرا می‌کند. `--build` باعث می‌شود imageها پیش از اجرا build شوند.

```
docker compose up -d
```

سرویس‌ها را در background اجرا می‌کند. `-d` مخفف detached mode است.

```
docker compose ps
```

وضعیت سرویس‌های Compose را نمایش می‌دهد.

```
docker compose down
```

containerها و network ساخته‌شده توسط Compose را حذف می‌کند؛ فایل‌های پروژه و `.env` را حذف نمی‌کند.

```
docker compose stop
```

سرویس‌ها را متوقف می‌کند، اما containerها را برای راه‌اندازی مجدد نگه می‌دارد.

```
docker compose start
```

containerهای متوقف‌شده را دوباره اجرا می‌کند.

تفاوت مهم در مصاحبه:

- `stop` و `start`: متوقف‌کردن و اجرای مجدد container موجود.
- `down` و `up`: حذف منابع Compose و ساخت مجدد آن‌ها هنگام اجرای دوباره.
- `up --build`: build کردن imageها پیش از اجرا.

### بررسی API

```
curl http://localhost:8000/hello
```

`curl` برای ارسال HTTP request از ترمینال استفاده می‌شود. این درخواست endpoint را فراخوانی می‌کند.

پاسخ:

```
{"message":"Hello from FastAPI"}
```

بررسی تنظیمات:

```
curl http://localhost:8000/config
```

پاسخ:

```
{"environment":"production","llm_model":"my-test-model"}
```

این تست نشان داد متغیرهای فایل `.env` به container منتقل شده‌اند.

## 2. ساخت سرویس دوم به نام AI Service

هدف: جداکردن منطق AI از API اصلی و آماده‌کردن معماری چندسرویسی.

ساخت پوشه:

```
mkdir -p ai-service
```

- `mkdir` پوشه می‌سازد.
- `-p` اجازه می‌دهد پوشه‌های لازم نیز ساخته شوند و در صورت وجود پوشه، خطا ایجاد نشود.

ساختار جدید:

```
n8n-learning/
├── compose.yaml
├── fastapi-basic/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── ai-service/
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
```

### فایل `ai-service/main.py`

```
from fastapi import FastAPIfrom pydantic import BaseModelapp = FastAPI()class AnalyzeRequest(BaseModel):    text: str@app.post("/analyze")def analyze(request: AnalyzeRequest):    return {        "result": f"AI analyzed: {request.text}",        "length": len(request.text),    }
```

توضیح:

- `FastAPI` برنامه API را می‌سازد.
- `BaseModel` از Pydantic ساختار و نوع داده ورودی را تعریف می‌کند.
- `AnalyzeRequest` مشخص می‌کند درخواست باید شامل فیلد `text` از نوع رشته باشد.
- `@app.post("/analyze")` یک endpoint برای HTTP POST تعریف می‌کند.
- `request.text` متن ارسالی را می‌خواند.
- `len()` طول متن را محاسبه می‌کند.
- خروجی dictionary به JSON تبدیل می‌شود.

نکته: این سرویس فعلاً شبیه‌ساز است؛ هنوز مدل LLM واقعی اجرا نمی‌کند.

### فایل `ai-service/requirements.txt`

```
fastapi[standard]
```

این dependencyها را برای اجرای FastAPI نصب می‌کند.

### فایل `ai-service/Dockerfile`

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

| دستور            | کاربرد                                             |
| ---------------- | -------------------------------------------------- |
| `FROM`           | تعیین image پایه؛ در اینجا Python 3.12 با نسخه سبک |
| `WORKDIR`        | تعیین پوشه کاری داخل container                     |
| `COPY`           | کپی فایل‌ها از محیط build به image                 |
| `RUN`            | اجرای دستور هنگام build شدن image                  |
| `pip install`    | نصب dependencyها                                   |
| `--no-cache-dir` | جلوگیری از نگهداری cache نصب پکیج‌ها               |
| `CMD`            | تعیین دستور پیش‌فرض اجرای container                |
| `--host 0.0.0.0` | گوش‌دادن برنامه روی interfaceهای container         |
| `--port 8000`    | اجرای سرور روی پورت ۸۰۰۰                           |

در این پروژه، `requirements.txt` جداگانه کپی و نصب می‌شود تا مراحل نصب dependencyها از کپی کد برنامه تفکیک شوند.

## 3. اضافه‌کردن سرویس دوم به Compose

فایل `compose.yaml` را به این شکل تغییر دادیم:

```

services:
  api:
    build: ./fastapi-basic
    container_name: fastapi-api
    ports:
      - "8000:8000"
    env_file:
      - ./fastapi-basic/.env
    depends_on:
      - ai-service

  ai-service:
    build: ./ai-service
    container_name: ai-service

```

نکات مهم:

- `ai-service` سرویس دوم است و image آن از پوشه `ai-service` ساخته می‌شود.
- `depends_on` مشخص می‌کند Compose ابتدا سرویس `ai-service` را شروع کند و سپس سرویس `api` را شروع کند.
- `depends_on` به‌تنهایی تضمین نمی‌کند که برنامه سرویس وابسته کاملاً آماده پاسخ‌گویی شده باشد.
- فقط سرویس `api` پورت خود را روی میزبان منتشر می‌کند. سرویس `ai-service` فعلاً از طریق شبکه داخلی Compose در دسترس است.

اجرای هر دو سرویس:

```
docker compose up -d --build
```

بررسی وضعیت:

```
docker compose ps
```

خروجی مورد انتظار شامل دو سرویس با وضعیت `Up` است:

```
fastapi-api
ai-service
```

## 4. ارتباط داخلی سرویس‌ها در Docker Compose

مفهوم کلیدی: سرویس‌های Compose به‌طور پیش‌فرض روی یک network مشترک قرار می‌گیرند و می‌توانند با نام سرویس یکدیگر را پیدا کنند.

ارتباط از داخل `fastapi-api` با سرویس دوم:

```
http://ai-service:8000
```

چرا `localhost` اشتباه است؟

- `localhost` داخل یک container به همان container اشاره می‌کند.
- `ai-service` نام سرویس در Compose است و برای دسترسی به سرویس دوم استفاده می‌شود.
- نیازی نیست پورت سرویس دوم روی میزبان منتشر شود تا سرویس اول بتواند به آن دسترسی داشته باشد.

### تست ارتباط

```
docker exec fastapi-api python -c "import urllib.request; print(urllib.request.urlopen('http://ai-service:8000/docs').status)"
```

توضیح:

- `docker exec` دستور را داخل یک container در حال اجرا اجرا می‌کند.
- `fastapi-api` نام container مقصد است.
- `python -c` کد Python کوتاه را مستقیماً اجرا می‌کند.
- `urllib.request.urlopen()` به صفحه مستندات سرویس دوم درخواست HTTP می‌فرستد.
- `.status` کد وضعیت پاسخ را نمایش می‌دهد.

پاسخ:

```
200
```

کد `200` نشان داد سرویس اصلی می‌تواند سرویس دوم را از طریق شبکه داخلی فراخوانی کند.

## 5. فراخوانی AI Service از FastAPI با HTTPX

هدف: به‌جای اجرای منطق تحلیل در API اصلی، درخواست را به سرویس دوم بفرستیم و پاسخ آن را برگردانیم.

### افزودن dependency

فایل `fastapi-basic/requirements.txt`:

```
fastapi[standard]
httpx
```

`httpx` یک کتابخانه Python برای ارسال HTTP request است.

### کد endpoint

در `fastapi-basic/main.py`، importهای موردنیاز:

```
import httpxfrom fastapi import FastAPIfrom pydantic import BaseModel
```

کلاس ورودی `AnalyzeRequest` همان مدلی است که قبلاً تعریف کرده بودیم. تابع `/analyze` را به این شکل تغییر دادیم:

```
@app.post("/analyze")async def analyze(request: AnalyzeRequest):    async with httpx.AsyncClient() as client:        response = await client.post(            "http://ai-service:8000/analyze",            json={"text": request.text},        )    return response.json()
```

توضیح خطوط جدید:

- `async def` تابع asynchronous تعریف می‌کند.
- `httpx.AsyncClient()` یک HTTP client غیرهمگام می‌سازد.
- `async with` تضمین می‌کند client پس از استفاده بسته شود.
- `await client.post(...)` درخواست POST را می‌فرستد و منتظر نتیجه آن می‌ماند، بدون اینکه عملیات انتظار به‌صورت blocking معمول اجرا شود.
- `json={"text": request.text}` داده را به شکل JSON در بدنه درخواست می‌فرستد.
- `response.json()` پاسخ JSON سرویس دوم را به داده Python تبدیل می‌کند.

### اجرای مجدد با dependency جدید

```
docker compose up -d --build
```

چون `requirements.txt` تغییر کرده بود، image مربوط به API باید دوباره build می‌شد.

### تست endpoint

```
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Docker makes AI systems easier to deploy."}'
```

توضیح گزینه‌ها:

- `-X POST`: تعیین روش HTTP.
- `-H`: تعیین HTTP header.
- `Content-Type: application/json`: اعلام می‌کند بدنه درخواست JSON است.
- `-d`: داده ارسالی در بدنه درخواست.

پاسخ موفق:

```
{
  "result": "AI analyzed: Docker makes AI systems easier to deploy.",
  "length": 41
}
```

جریان درخواست اکنون چنین است:

```
Client
  ↓ POST /analyze
FastAPI API
  ↓ HTTP POST
AI Service
  ↓ JSON response
FastAPI API
  ↓ JSON response
Client
```

## 6. مدیریت خطا و Timeout

هدف: جلوگیری از انتظار نامحدود و تبدیل خطاهای سرویس AI به پاسخ‌های HTTP قابل‌فهم برای client.

در `fastapi-basic/main.py`، import مربوط به FastAPI باید شامل `HTTPException` باشد:

```
import httpxfrom fastapi import FastAPI, HTTPExceptionfrom pydantic import BaseModel
```

تابع `/analyze` را به نسخه زیر تغییر دادیم:

```
@app.post("/analyze")async def analyze(request: AnalyzeRequest):    try:        async with httpx.AsyncClient(timeout=5.0) as client:            response = await client.post(                "http://ai-service:8000/analyze",                json={"text": request.text},            )        response.raise_for_status()        return response.json()    except httpx.TimeoutException:        raise HTTPException(            status_code=504,            detail="AI service timed out",        )    except httpx.HTTPStatusError:        raise HTTPException(            status_code=502,            detail="AI service returned an error",        )    except httpx.RequestError:        raise HTTPException(            status_code=503,            detail="AI service is unavailable",        )
```

توضیح:

- `try` بلوکی است که خطاهای مورد انتظار آن را مدیریت می‌کنیم.
- `timeout=5.0` برای عملیات HTTP محدودیت زمانی ۵ ثانیه‌ای تعیین می‌کند.
- `raise_for_status()` برای پاسخ‌های HTTP ناموفق با کد 4xx یا 5xx، exception ایجاد می‌کند.
- `HTTPException` به FastAPI اجازه می‌دهد پاسخ HTTP با status code و پیام مشخص برگرداند.
- `except` خطاهای مشخص را دریافت و مدیریت می‌کند.

### نگاشت خطاها

| خطا                      | پاسخ API                  | معنی                                   |
| ------------------------ | ------------------------- | -------------------------------------- |
| `httpx.TimeoutException` | `504 Gateway Timeout`     | سرویس در محدوده زمانی پاسخ نداده است   |
| `httpx.HTTPStatusError`  | `502 Bad Gateway`         | سرویس مقصد پاسخ HTTP ناموفق داده است   |
| `httpx.RequestError`     | `503 Service Unavailable` | خطا در برقراری ارتباط یا ارسال درخواست |

این سه حالت را نباید با هم اشتباه گرفت. برای مثال، `503` در این پیاده‌سازی نشان‌دهنده خطای ارتباطی است؛ نه هر خطایی که سرویس مقصد برگرداند.

پس از تغییر کد:

```
docker compose up -d --build
```

### تست حالت سالم

```
curl -i -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Docker makes AI systems easier to deploy."}'
```

گزینه `-i` علاوه بر بدنه پاسخ، HTTP headers و status code را نیز نمایش می‌دهد.

انتظار:

```
HTTP/1.1 200 OK
```

### تست از دسترس خارج شدن AI Service

ابتدا سرویس دوم را متوقف کردیم:

```
docker compose stop ai-service
```

سپس درخواست را دوباره فرستادیم:

```
curl -i -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Test when AI service is down."}'
```

پاسخ مشاهده‌شده:

```
HTTP/1.1 503 Service Unavailable
```

سرویس دوم را دوباره راه‌اندازی کردیم:

```
docker compose start ai-service
```

و وضعیت سرویس‌ها را بررسی کردیم:

```
docker compose ps
```

هر دو سرویس `Up` بودند. درخواست مجدد به `/analyze` نیز پاسخ `200 OK` برگرداند.

## 7. معماری فعلی پروژه

Client

HTTP POST /analyze

FastAPI — `api`

Port 8000 · Input validation · HTTPX · Timeout · Error handling

HTTP · `http://ai-service:8000/analyze`

AI Service — `ai-service`

Port 8000 داخل شبکه Compose · تحلیل آزمایشی متن · JSON response

نکته: پورت ۸۰۰۰ هر دو container یکسان است، اما تداخلی ندارند؛ هر container شبکه و فضای پورت مستقل خود را دارد. فقط پورت API اصلی روی میزبان منتشر شده است.

## 8. جمع‌بندی برای مصاحبه

باید بتوانی این موارد را بدون مراجعه به راهنما توضیح بدهی:

1. Docker Compose چیست؟ ابزاری برای تعریف و اجرای چند سرویس مرتبط از طریق یک فایل پیکربندی.
2. چرا سرویس دوم ساختیم؟ برای جداکردن AI logic از API اصلی و ایجاد مرز مشخص بین سرویس‌ها.
3. چرا از `http://ai-service:8000` استفاده کردیم؟ چون نام سرویس در شبکه داخلی Compose قابل resolve شدن است؛ `localhost` داخل container به همان container اشاره می‌کند.
4. چرا `httpx` استفاده کردیم؟ برای ارسال HTTP request از FastAPI به سرویس دیگر.
5. چرا `async` و `await` استفاده کردیم؟ برای انتظار غیرهمگام هنگام انجام عملیات شبکه.
6. Timeout چه کاربردی دارد؟ محدودکردن مدت انتظار برای پاسخ.
7. چرا `raise_for_status()` مهم است؟ تا پاسخ HTTP ناموفق به‌عنوان خطا تشخیص داده شود.
8. چرا خطاها را به 502، 503 و 504 نگاشت کردیم؟ تا client بتواند نوع کلی شکست درخواست را از status code تشخیص دهد.
9. چطور خرابی سرویس را تست کردیم؟ سرویس AI را با `docker compose stop` متوقف کردیم، پاسخ 503 را بررسی کردیم و با `docker compose start` دوباره راه‌اندازی کردیم.

وضعیت فعلی: دو سرویس Compose اجرا می‌شوند؛ API اصلی درخواست را با HTTPX به AI Service می‌فرستد و خطاهای اصلی ارتباط مدیریت می‌شوند. مرحله بعدی طبق مسیر یادگیری، اتصال n8n به همین API است.