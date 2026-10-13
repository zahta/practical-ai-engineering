# Tutorial: ساخت یک Workflow کاربردی با n8n، FastAPI و Docker

در این پروژه، یک workflow می‌سازیم که درخواست HTTP دریافت می‌کند، متن را اعتبارسنجی می‌کند، آن را به API می‌فرستد و بر اساس نتیجه، پاسخ مناسب برمی‌گرداند.

## ۱. معماری پروژه

Client — `curl`

ارسال درخواست POST و متن در قالب JSON

n8n Webhook

دریافت درخواست HTTP

IF

بررسی معتبر بودن متن

True

HTTP Request

فراخوانی FastAPI

Respond to Webhook

False

Respond to Webhook

بازگرداندن خطای 400

Docker Compose

اجرای n8n، FastAPI و سرویس AI در شبکهٔ مشترک

سرویس AI در این پروژه فعلاً Mock است؛ یعنی مدل زبانی واقعی اجرا نمی‌کند و صرفاً نتیجه‌ای آزمایشی برمی‌گرداند.

## ۲. محیط اجرا و Docker Compose

محیط پروژه، Ubuntu در WSL2 روی ویندوز است و Docker Desktop از قبل نصب و فعال شده است. بنابراین نیازی به نصب مجدد Docker داخل Ubuntu نداریم.

دایرکتوری پروژه:

```
cd ~/n8n-learning
```

- `cd`: تغییر دایرکتوری کاری ترمینال.
- `~`: دایرکتوری خانگی کاربر لینوکس.

### فایل `compose.yaml`

Docker Compose سرویس‌های پروژه را با یک فایل پیکربندی اجرا و مدیریت می‌کند.

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

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      N8N_SECURE_COOKIE: "false"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - api
    restart: unless-stopped

volumes:
  n8n_data:
```

### معنی بخش‌های مهم

| تنظیم                     | مفهوم                                                              |
| ------------------------- | ------------------------------------------------------------------ |
| `services`                | تعریف سرویس‌ها یا کانتینرهای پروژه                                 |
| `build`                   | ساخت image از Dockerfile موجود در مسیر مشخص                        |
| `image`                   | استفاده از image آماده                                             |
| `container_name`          | تعیین نام مشخص برای کانتینر                                        |
| `ports`                   | نگاشت پورت میزبان به پورت کانتینر                                  |
| `env_file`                | بارگذاری متغیرهای محیطی از فایل                                    |
| `environment`             | تعریف متغیر محیطی در Compose                                       |
| `volumes`                 | نگهداری داده‌ها خارج از چرخهٔ عمر کانتینر                          |
| `depends_on`              | تعیین وابستگی اولیهٔ سرویس‌ها                                      |
| `restart: unless-stopped` | راه‌اندازی مجدد کانتینر پس از توقف، مگر اینکه عمداً متوقف شده باشد |

برای مثال:

```
ports:
  - "5678:5678"
```

یعنی پورت `5678` روی میزبان به پورت `5678` در کانتینر متصل است؛ بنابراین رابط n8n در آدرس `http://localhost:5678` قابل دسترسی است.

گزینهٔ `N8N_SECURE_COOKIE: "false"` در این پروژه فقط برای استفادهٔ محلی با HTTP تنظیم شده است. برای استقرار عمومی، باید HTTPS و تنظیمات امن مناسب استفاده شوند.

### اجرای سرویس‌ها

```
docker compose up -d
```

- `docker compose`: مدیریت سرویس‌های تعریف‌شده در فایل Compose.
- `up`: ایجاد و راه‌اندازی سرویس‌ها.
- `-d`: اجرا در پس‌زمینه.

بررسی وضعیت:

```
docker compose ps
```

نمایش لاگ‌های n8n:

```
docker compose logs -f n8n
```

- `logs`: نمایش گزارش اجرای کانتینر.
- `-f`: دنبال‌کردن زندهٔ لاگ‌ها.

## ۳. تفاوت `localhost` با نام سرویس در Docker

این مفهوم برای اتصال n8n به FastAPI ضروری است.

- از مرورگر ویندوز یا WSL، برای دسترسی به n8n از `http://localhost:5678` استفاده می‌کنیم.
- از داخل کانتینر n8n، برای فراخوانی FastAPI از `http://api:8000` استفاده می‌کنیم.
- برای دسترسی به سرویس AI از کانتینر دیگر، از `http://ai-service:8000` استفاده می‌کنیم.

در شبکهٔ Docker Compose، نام سرویس نقش hostname را دارد.

چرا `localhost:8000` داخل n8n اشتباه است؟ چون `localhost` در کانتینر n8n به خود همان کانتینر اشاره می‌کند، نه کانتینر FastAPI.

## ۴. سرویس FastAPI و endpoint تحلیل متن

در این پروژه، API در مسیر `fastapi-basic` قرار دارد و endpoint زیر را ارائه می‌دهد:

```
response = await client.post(    "http://ai-service:8000/analyze",    json={"text": request.text},    timeout=5.0,)response.raise_for_status()return response.json()
```

این قطعه، منطق اصلی ارتباط API با سرویس AI را نشان می‌دهد.

- `client.post(...)`: ارسال درخواست HTTP از نوع POST.
- `json={...}`: ارسال بدنهٔ درخواست به شکل JSON.
- `request.text`: متن دریافتی از درخواست کاربر.
- `timeout=5.0`: حداکثر زمان انتظار برای پاسخ، برحسب ثانیه.
- `raise_for_status()`: در صورت دریافت پاسخ HTTP ناموفق، خطا ایجاد می‌کند.
- `response.json()`: بدنهٔ پاسخ JSON را به دادهٔ قابل‌استفاده در Python تبدیل می‌کند.

مدیریت خطاهای این API نیز اهمیت دارد:

| خطا                            | وضعیت HTTP                |
| ------------------------------ | ------------------------- |
| Timeout از سرویس AI            | `504 Gateway Timeout`     |
| پاسخ HTTP ناموفق از سرویس AI   | `502 Bad Gateway`         |
| خطای ارتباط یا دسترسی به سرویس | `503 Service Unavailable` |

این وضعیت‌ها کمک می‌کنند مصرف‌کنندهٔ API تشخیص دهد درخواست چرا ناموفق بوده است.

## ۵. راه‌اندازی اولیهٔ n8n

در مرورگر باز کن:

`http://localhost:5678`

در اولین ورود، حساب مالک محلی را ایجاد کن و وارد محیط n8n شو.

### مفاهیم پایهٔ رابط n8n

- Workflow: مجموعه‌ای از نودهای متصل که یک فرایند خودکار را تشکیل می‌دهند.
- Node: یک مرحله از فرایند؛ مانند دریافت Webhook یا ارسال درخواست HTTP.
- Connection: خط اتصال خروجی یک نود به ورودی نود بعدی؛ تعیین می‌کند داده از کدام مسیر عبور کند.
- Execution: یک نوبت اجرای workflow که ورودی‌ها، خروجی‌ها و خطاهای آن قابل بررسی است.
- Trigger: نودی که اجرای workflow را آغاز می‌کند؛ مانند Manual Trigger یا Webhook.

## ۶. ساخت اولین Workflow: Manual Trigger → HTTP Request

ابتدا یک workflow جدید بساز و دو نود به آن اضافه کن.

### نود اول: Manual Trigger

این نود اجرای آزمایشی workflow را با اقدام دستی آغاز می‌کند.

### نود دوم: HTTP Request

تنظیمات:

| فیلد              | مقدار                     |
| ----------------- | ------------------------- |
| Method            | `POST`                    |
| URL               | `http://api:8000/analyze` |
| Send Body         | فعال                      |
| Body Content Type | `JSON`                    |
| Specify Body      | `Using JSON`              |

در بخش JSON:

```
{
  "text": "Hello from my first n8n AI workflow!"
}
```

معنی تنظیمات: `POST` برای ارسال داده به API است. آدرس، endpoint سرویس FastAPI را مشخص می‌کند. بدنهٔ JSON حاوی فیلد `text` است که سرویس AI باید آن را پردازش کند.

اتصال نودها:

`Manual Trigger → HTTP Request`

سپس workflow را با دکمهٔ اجرای آزمایشی کل workflow اجرا کن.

### خروجی مورد انتظار

```
{
  "result": "AI analyzed: Hello from my first n8n AI workflow!",
  "length": 36
}
```

فیلد `result` متن نتیجه را برمی‌گرداند و `length` تعداد کاراکترهای متن ورودی را نشان می‌دهد.

خروجی را در بخش Executions باز کن و نود HTTP Request را انتخاب کن.

## ۷. ساخت Workflow مبتنی بر Webhook

Manual Trigger برای آزمایش دستی مناسب است؛ اما برای اجرای خودکار در پاسخ به درخواست خارجی، از Webhook استفاده می‌کنیم.

Workflow جدید بساز و دو نود زیر را متصل کن:

`Webhook → HTTP Request`

### تنظیمات Webhook

| فیلد           | مقدار          |
| -------------- | -------------- |
| HTTP Method    | `POST`         |
| Path           | `analyze-text` |
| Authentication | `None`         |
| Respond        | `Immediately`  |

- HTTP Method: نوع درخواست قابل‌قبول.
- Path: مسیر اختصاصی Webhook.
- Authentication: روش احراز هویت؛ در این تمرین محلی غیرفعال است.
- Respond: تعیین می‌کند پاسخ HTTP چه زمانی برگردد.

`Authentication: None` فقط برای این تمرین محلی است؛ برای یک endpoint عمومی باید احراز هویت و کنترل دسترسی مناسب در نظر گرفته شود.

### تنظیمات HTTP Request

تنظیمات همان بخش قبل است، با این تفاوت که متن از ورودی Webhook گرفته می‌شود.

```
{
  "text": "{{ $json.body.text }}"
}
```

در اینجا:

- `$json`: دادهٔ ورودی فعلی نود.
- `body`: بدنهٔ درخواست Webhook.
- `text`: فیلد متن داخل JSON ورودی.
- `{{ ... }}`: ارزیابی عبارت به‌عنوان Expression در n8n.

برای نمونه، ورودی زیر:

```
{
  "text": "Run AI automation through a webhook."
}
```

در خروجی Webhook به‌صورت زیر قابل دسترسی است:

```
$json.body.text
```

بنابراین Expression، متن را استخراج می‌کند و در بدنهٔ درخواست به FastAPI قرار می‌دهد.

## ۸. آزمایش Webhook در حالت Test

در نود Webhook روی Listen for Test Event کلیک کن. این گزینه Webhook را برای دریافت یک درخواست آزمایشی آماده می‌کند.

در ترمینال WSL اجرا کن:

```
curl -X POST "http://localhost:5678/webhook-test/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text":"Run AI automation through a webhook."}'
```

### معنی اجزای دستور

- `curl`: ارسال درخواست HTTP از ترمینال.
- `-X POST`: مشخص‌کردن متد POST.
- `-H`: تنظیم HTTP header؛ در اینجا اعلام می‌کنیم بدنه JSON است.
- `-d`: داده‌ای که در بدنهٔ درخواست ارسال می‌شود.
- `webhook-test`: مسیر مخصوص Webhook در حالت آزمایشی.

در این حالت، ممکن است ترمینال پاسخی مانند زیر دریافت کند:

```
{
  "message": "Workflow was started"
}
```

با تنظیم `Respond: Immediately` این پاسخ اولیه طبیعی است. نتیجهٔ نهایی API را در خروجی نود HTTP Request در Executions مشاهده می‌کنی.

### نکتهٔ مهم دربارهٔ اجرای نودها

در اجرای عادی یک workflow، نودهای متصل طبق مسیر اجرا می‌شوند. کلیک روی آیکون اجرای دستی یک نود با اجرای کل workflow یکسان نیست.

اگر ورودی Webhook دریافت شده اما HTTP Request اجرا نشده است، بررسی کن که:

1. اتصال خروجی Webhook به ورودی HTTP Request برقرار باشد.
2. نود HTTP Request در همان Execution قرار داشته باشد و خطا یا محدودیت مسیر مانع اجرای آن نشده باشد.
3. اجرای کل workflow از روش مناسب آغاز شده باشد.

## ۹. اجرای خودکار با Production Webhook

برای استفاده از Webhook خارج از حالت آزمایشی:

1. workflow را ذخیره کن.
2. آن را با گزینهٔ Publish یا Activate فعال کن؛ نام گزینه بسته به نسخهٔ n8n متفاوت است.
3. در نود Webhook، بخش Production URL را باز کن.

آدرس Production در این پروژه:

`http://localhost:5678/webhook/analyze-text`

تفاوت دو URL:

| حالت       | مسیر                         |
| ---------- | ---------------------------- |
| Test       | `/webhook-test/analyze-text` |
| Production | `/webhook/analyze-text`      |

آدرس Production برای workflow فعال است و نیازی به کلیک روی Listen for Test Event ندارد.

دستور تست:

```
curl -X POST "http://localhost:5678/webhook/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text":"Production webhook works!"}'
```

خروجی مورد انتظار در HTTP Request:

```
{
  "result": "AI analyzed: Production webhook works!",
  "length": 25
}
```

عدد `25` طول متن `Production webhook works!` است.

## ۱۰. اضافه‌کردن اعتبارسنجی با نود IF

اکنون workflow را گسترش می‌دهیم تا متن خالی به سرویس AI ارسال نشود.

مسیر قبلی:

`Webhook → HTTP Request`

مسیر جدید:

`Webhook → IF → HTTP Request`

نود `IF` یک شرط را ارزیابی می‌کند و داده را از یکی از دو خروجی می‌فرستد:

- `true`: شرط برقرار است.
- `false`: شرط برقرار نیست.

### تنظیمات IF

در نود IF، یک شرط رشته‌ای تنظیم کن:

| فیلد     | مقدار                   |
| -------- | ----------------------- |
| Value 1  | `{{ $json.body.text }}` |
| Operator | `String → is not empty` |

در بعضی نسخه‌ها نام یا محل گزینه‌ها کمی متفاوت است؛ معیار این است که شرط بررسی کند متن خالی نباشد.

اتصال‌ها:

- خروجی Webhook به ورودی IF
- خروجی `true` از IF به HTTP Request
- خروجی `false` فعلاً بدون اتصال

### آزمایش متن معتبر

```
curl -X POST "http://localhost:5678/webhook/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text":"Test IF node"}'
```

نتیجهٔ مورد انتظار:

```
{
  "result": "AI analyzed: Test IF node",
  "length": 12
}
```

در Execution باید مسیر `true` و نود HTTP Request اجرا شده باشند.

### آزمایش متن خالی

```
curl -X POST "http://localhost:5678/webhook/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text":""}'
```

در Execution، نود IF باید مسیر `false` را انتخاب کند و HTTP Request اجرا نشود.

این رفتار باعث می‌شود ورودی نامعتبر پیش از فراخوانی API فیلتر شود.

## ۱۱. برگرداندن پاسخ واقعی به درخواست‌کننده

تا اینجا درخواست‌کننده می‌تواند وضعیت اجرای workflow را دریافت کند، اما هنوز پاسخ نهایی سرویس AI یا خطای اعتبارسنجی را مستقیماً دریافت نمی‌کند.

برای مدیریت پاسخ، از نود Respond to Webhook استفاده می‌کنیم.

### تغییر تنظیمات Webhook

در نود Webhook:

| فیلد    | مقدار                           |
| ------- | ------------------------------- |
| Respond | `Using Respond to Webhook Node` |

این تنظیم باعث می‌شود نود Respond to Webhook مسئول برگرداندن پاسخ HTTP باشد.

### مسیر موفق: `true`

دو نود را به این ترتیب متصل کن:

`IF (true) → HTTP Request → Respond to Webhook`

نود Respond مربوط به مسیر موفق را تنظیم کن:

| فیلد          | مقدار                            |
| ------------- | -------------------------------- |
| Respond With  | `JSON`                           |
| Response Body | `{{ $json }}` در حالت Expression |
| Response Code | `200`                            |

Expression زیر:

```
{{ $json }}
```

دادهٔ JSON ورودی نود Respond را برمی‌گرداند. چون این نود بعد از HTTP Request قرار دارد، دادهٔ ورودی آن خروجی FastAPI است.

پاسخ نمونه:

```
{
  "result": "AI analyzed: Hello from n8n",
  "length": 15
}
```

### مسیر نامعتبر: `false`

اتصال مسیر دوم:

`IF (false) → Respond to Webhook`

تنظیمات:

| فیلد          | مقدار  |
| ------------- | ------ |
| Respond With  | `JSON` |
| Response Code | `400`  |

در Response Body، این JSON را قرار بده:

```
{
  "error": "Text must not be empty"
}
```

کد وضعیت `400 Bad Request` نشان می‌دهد که درخواست به دلیل نامعتبر بودن ورودی پذیرفته نشده است.

## ۱۲. تست نهایی هر دو مسیر

برای مشاهدهٔ کد وضعیت HTTP، از گزینهٔ `-i` در curl استفاده می‌کنیم. این گزینه headerهای پاسخ را نیز نمایش می‌دهد.

### تست اول: متن معتبر

```
curl -i -X POST "http://localhost:5678/webhook/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from n8n"}'
```

پاسخ مورد انتظار:

```
HTTP/1.1 200 OK
Content-Type: application/json
```

```
{
  "result": "AI analyzed: Hello from n8n",
  "length": 15
}
```

### تست دوم: متن خالی

```
curl -i -X POST "http://localhost:5678/webhook/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text":""}'
```

پاسخ مورد انتظار:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
```

```
{
  "error": "Text must not be empty"
}
```

این دو تست را با موفقیت اجرا کردیم. بنابراین هر دو مسیر workflow به‌درستی کار می‌کنند.

## ۱۳. نمای کلی Workflow نهایی

Webhook

POST /webhook/analyze-text

IF: text is not empty

true

HTTP Request

POST به FastAPI

Respond to Webhook

200 + نتیجهٔ JSON

false

Respond to Webhook

400 + پیام خطا

## ۱۴. نکات عملیاتی مهم

- 🟢 آدرس داخلی Docker: برای ارتباط کانتینرها از نام سرویس، مانند `http://api:8000` استفاده کن.
- 🟢 Production Webhook: workflow باید فعال باشد و درخواست به URL تولید ارسال شود.
- 🟢 پاسخ HTTP: با `Respond to Webhook` می‌توان هم بدنهٔ پاسخ و هم کد وضعیت را کنترل کرد.
- 🟡 امنیت: احراز هویت و HTTPS برای Webhook عمومی ضروری‌اند؛ تنظیمات این تمرین برای توسعهٔ محلی است.
- 🟡 خطاهای API: در پروژهٔ واقعی، خطای HTTP Request یا timeout سرویس AI نیز باید مدیریت شود.
- 🟡 سرویس واقعی AI: سرویس فعلی Mock است. برای تحلیل واقعی متن، باید آن را با یک مدل زبانی واقعی جایگزین کنیم.

این پایان بخش n8n در پروژهٔ فعلی است: از دریافت درخواست HTTP و اجرای خودکار گرفته تا اعتبارسنجی ورودی، فراخوانی API و برگرداندن پاسخ موفق یا خطا.