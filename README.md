<div align="center">

# 📊 Traffic Analyzer

### 🌐 Self-Hosted Web Analytics Platform

**A powerful, open-source alternative to Google Analytics — built with Django**

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Redis](https://img.shields.io/badge/Redis-Memurai-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[Features](#-features) • [Installation](#-installation) • [How to Login](#-how-to-login) • [File Structure](#️-file-structure) • [Troubleshooting](#-troubleshooting)

</div>

---

## 🎯 What is Traffic Analyzer?

**Traffic Analyzer** হলো একটা **self-hosted web analytics platform** যা Django দিয়ে বানানো। আপনি এটি ব্যবহার করে আপনার website এর visitor traffic track করতে পারবেন — **Google Analytics এর মতো**, কিন্তু **সম্পূর্ণ আপনার control এ**, এবং **free**।

### ✨ কেন এই Project?

| 🎯 Feature | 💡 Benefit |
|-----------|-----------|
| **Self-Hosted** | আপনার data আপনার কাছে |
| **Real-time** | Live visitor count, world map এ position |
| **Privacy-First** | GDPR-friendly, no 3rd-party tracking |
| **Customizable** | Full source code access |
| **Free Forever** | No subscription, no API limit |

---

## ✨ Features

<details open>
<summary><b>📈 Analytics — সব traffic data এক জায়গায়</b></summary>

- 🖱️ **Page View Tracking** — JavaScript snippet দিয়ে যেকোনো website track
- 👤 **Unique Visitor Detection** — Cookie-based identification
- 📉 **Bounce Rate Calculation** — Single-page visits measure
- 🖥️ **Browser Detection** — Chrome, Firefox, Safari, Edge
- 💻 **OS Detection** — Windows, macOS, Linux, Android, iOS
- 📱 **Device Breakdown** — Desktop, Mobile, Tablet
- 🌍 **GeoIP Location** — Country detection (MaxMind GeoLite2)

</details>

<details open>
<summary><b>⚡ Real-Time — live visitors এখনি দেখুন</b></summary>

- 🔴 **Live Visitor Count** — Redis/Memurai powered real-time counter
- 👥 **Active Visitors Panel** — কারা এখন site এ আছে
- 🗺️ **Live World Map** — Leaflet.js দিয়ে visitor দের geographic location
- 🔄 **Auto-Refresh** — প্রতি 5 seconds এ update

</details>

<details open>
<summary><b>🎯 Advanced Tracking</b></summary>

- 🎪 **Custom Events** — Button clicks, purchases, video plays track
- 🤖 **Auto-Tracking** — Form submits, outbound links স্বয়ংক্রিয়ভাবে track
- 📊 **Event Analytics** — কোন event কতবার trigger হচ্ছে
- 🎨 **Session Tracking** — Visitor দের session duration

</details>

<details open>
<summary><b>📊 Reports & Export</b></summary>

- 📈 **Interactive Dashboard** — Chart.js দিয়ে beautiful charts
- 🎨 **Per-Website Analytics** — প্রতিটা website এর আলাদা dashboard
- 📥 **CSV Export** — PageViews, Visitors, Stats download
- 📧 **Email Reports** — Daily/Weekly/Monthly automatic emails (Celery)
- 🔔 **Scheduled Reports** — Custom time এ email পাবেন

</details>

<details open>
<summary><b>🔌 REST API — external tools এর জন্য</b></summary>

- 🔑 **API Key Authentication** — Per-website token
- 🚦 **Rate Limiting** — 1000 requests/hour
- 📚 **RESTful Endpoints** — Stats, Visitors, PageViews, Realtime
- 📖 **JSON Responses** — Standard API format

</details>

<details open>
<summary><b>🎨 Modern UI</b></summary>

- 🌙 **Dark Mode** — localStorage-supported toggle
- 📱 **Fully Responsive** — Mobile, tablet, desktop
- ✨ **Smooth Animations** — Number counters, transitions
- 🔔 **Toast Notifications** — Non-intrusive alerts
- 🎯 **Sidebar Navigation** — Collapsible, mobile-friendly

</details>

---

## 🛠️ Tech Stack

<div align="center">

| **Backend** | **Frontend** | **Infrastructure** |
|:-----------:|:------------:|:------------------:|
| 🐍 Python 3.11+ | 🎨 Bootstrap 5 | 🔴 Redis / Memurai |
| 🎯 Django 5.x | 📊 Chart.js | ⚡ Celery |
| 🔌 DRF | 🗺️ Leaflet.js | 📬 SMTP Email |
| 🌍 GeoIP2 | 💅 Custom CSS | 🗄️ SQLite / PostgreSQL |

</div>

---

## 🚀 Installation

### 📋 Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| 🐍 **Python** | 3.11+ | `python --version` |
| 📦 **pip** | Latest | `pip --version` |
| 🔴 **Redis/Memurai** | Any | `memurai-cli ping` |
| 🔧 **Git** | Latest | `git --version` |

### 📥 Step 1: Clone Repository

```bash
git clone https://github.com/ratuuulhasan/traffic-analyzer.git
cd traffic-analyzer
```

### 🐍 Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ Terminal এ `(venv)` দেখলে সফল।

### 📦 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔴 Step 4: Setup Redis (Memurai on Windows)

**Windows এ:**

1. [Memurai Download](https://www.memurai.com/get-memurai) করুন
2. Install করুন (default settings)
3. Services.msc এ **Memurai** running কিনা দেখুন

**Verify:**
```bash
memurai-cli ping
# Output: PONG
```

**Linux / macOS:**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
```

### 🔐 Step 5: Environment Variables

Project root এ **`.env`** file বানান:

```env
# ========== Django ==========
SECRET_KEY=your-super-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# ========== Email (Gmail) ==========
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-digit-app-password
DEFAULT_FROM_EMAIL=Traffic Analyzer <your-email@gmail.com>
SITE_URL=http://127.0.0.1:8000

# ========== Redis ==========
REDIS_URL=redis://127.0.0.1:6379/0
```

#### 📧 Gmail App Password কিভাবে পাবেন?

1. https://myaccount.google.com/security এ যান
2. **2-Step Verification** enable করুন
3. https://myaccount.google.com/apppasswords এ যান
4. App name: **"Traffic Analyzer"** → **Generate**
5. 16-digit password copy করুন → `.env` এ paste করুন

> ⚠️ **গুরুত্বপূর্ণ:** `.env` file কখনো GitHub এ push করবেন না!

### 🗄️ Step 6: Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 🎨 Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 🌍 Step 8: GeoIP Setup (Optional)

Country detection এর জন্য:

1. [MaxMind Signup](https://www.maxmind.com/en/geolite2/signup) — ফ্রি account
2. **GeoLite2-Country.mmdb** download করুন
3. Root folder এ **`geoip/`** folder বানান
4. File টা `geoip/GeoLite2-Country.mmdb` এ রাখুন

---

## 🎬 Running the Project

> ⚠️ **গুরুত্বপূর্ণ:** Full functionality এর জন্য **৩টা terminal** একসাথে চালু রাখতে হবে।

### 🖥️ Terminal 1 — Django Server

```bash
python manage.py runserver
```

🌐 Access: `http://127.0.0.1:8000`

### 🖥️ Terminal 2 — Celery Worker

```bash
# Windows
celery -A config worker -l info --pool=solo

# Linux / macOS
celery -A config worker -l info
```

📧 Email reports generate ও send করবে।

### 🖥️ Terminal 3 — Celery Beat

```bash
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

⏰ Scheduled task trigger করবে।

### 💡 শুধু Tracking দেখতে চাইলে?

শুধু **Terminal 1** + **Redis (Memurai)** চালু থাকলেই হবে।

---

## 🔐 How to Login

### 🆕 First Time Registration

```
1. Browser খুলুন → http://127.0.0.1:8000
2. উপরে ডানে "Register" button click
3. Username, Email, Password দিন
4. Register চাপলে Automatic Login হবে → Dashboard এ যাবে
```

### 🔑 Regular Login

```
URL: http://127.0.0.1:8000/accounts/login/
Username: আপনার username
Password: আপনার password
```

### 👑 Admin Panel

```
URL: http://127.0.0.1:8000/admin/
Credentials: createsuperuser এর credentials
```

Admin panel থেকে manage করা যাবে:

| Item | কী দেখতে পাবেন |
|------|----------------|
| 👥 **Users** | সব registered users |
| 🌐 **Websites** | সব websites + API keys |
| 📊 **PageViews** | সব page view logs |
| 👤 **Visitors** | Unique visitors |
| 🎯 **Events** | Custom events |
| 📧 **Email Reports** | Report settings |
| ⏰ **Periodic Tasks** | Celery Beat schedule |

### 🚪 Logout

Navbar এ ডানে user dropdown → **Logout** অথবা:
```
http://127.0.0.1:8000/accounts/logout/
```

---

## 🗺️ File Structure

```
traffic_analyzer/
│
├── 📄 manage.py                  ← Django management
├── 📄 requirements.txt           ← Python packages
├── 🔐 .env                       ← Secrets (git ignored)
├── 🗄️ db.sqlite3                 ← Database
├── 📘 README.md                  ← এই file
│
├── ⚙️ config/                    ← Project settings
│   ├── settings.py               ← সব configuration
│   ├── urls.py                   ← Main URL routes
│   ├── celery.py                 ← Celery config
│   └── wsgi.py                   ← Deployment entry
│
├── 👤 accounts/                  ← User auth
│   ├── views.py                  ← Register/Login/Logout
│   └── urls.py
│
├── 🌐 websites/                  ← Website management
│   ├── models.py                 ← Website, APIKey, EmailReport
│   ├── views.py                  ← CRUD, Export, Events
│   ├── forms.py                  ← WebsiteForm
│   ├── tasks.py                  ← Celery email tasks
│   └── urls.py
│
├── 📊 analytics/                 ← Tracking & Analytics
│   ├── models.py                 ← Visitor, PageView, Event
│   ├── views.py                  ← Tracking API, Stats
│   ├── realtime.py               ← Redis real-time
│   ├── country_coords.py         ← Country → lat/lng
│   ├── urls.py
│   └── 🔌 api/                   ← Public REST API
│       ├── authentication.py     ← API Key auth
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── 🏠 dashboard/                 ← Dashboard
│   ├── views.py
│   └── urls.py
│
├── 🎨 templates/                 ← HTML templates
│   ├── base.html                 ← Main layout
│   ├── auth_base.html            ← Login layout
│   ├── dashboard/home.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── websites/
│   │   ├── website_list.html
│   │   ├── website_detail.html
│   │   ├── website_events.html
│   │   ├── website_map.html
│   │   └── email_settings.html
│   └── emails/
│       └── daily_report.html
│
├── 🎨 static/                    ← Static assets
│   ├── css/
│   │   ├── main.css
│   │   └── auth.css
│   ├── js/
│   │   └── main.js
│   └── tracking.js               ← ⭐ Tracking script
│
├── 🌍 geoip/                     ← MaxMind DB
│   └── GeoLite2-Country.mmdb
│
└── 🖼️ media/                     ← User uploads
```

---

## 🎯 How Each Feature Works

### 📌 1. Tracking System

```
[User's Website]
      ↓
[tracking.js loads]  ← script paste করা
      ↓
[POST /api/track/]   ← visitor data পাঠায়
      ↓
[Django View]
  • User-Agent parse (browser/OS/device)
  • IP → GeoIP (country)
  • Visitor + PageView save
  • Redis এ mark real-time
      ↓
[Dashboard এ দেখায়]
```

**Files:**
- 🎨 `static/tracking.js` — Client-side
- 🐍 `analytics/views.py` → `track_view()` — Server handler
- 💾 `analytics/models.py` → `Visitor`, `PageView`
- ⚡ `analytics/realtime.py` — Redis logic

### 📌 2. Real-Time Visitors

```
[Every track request]
      ↓
[mark_visitor_active()]  ← Redis এ save
      ↓
[5-minute TTL]
      ↓
[Dashboard polls /api/realtime/ every 5s]
      ↓
[Redis থেকে active list → UI update]
```

**Files:**
- ⚡ `analytics/realtime.py`
- 🐍 `analytics/views.py` → `realtime_api()`

### 📌 3. Email Reports

```
[Celery Beat — প্রতি ঘন্টা]
      ↓
[check_and_send_reports task]
      ↓
[Hour match?] → YES
      ↓
[HTML email generate]
      ↓
[SMTP (Gmail) → User's inbox]
      ↓
[last_sent update]
```

**Files:**
- 🐍 `websites/tasks.py`
- 💾 `websites/models.py` → `EmailReportSetting`
- 🎨 `templates/emails/`

### 📌 4. Custom Events

**Auto-tracking:**
- 📝 Form submit → `form_submit`
- 🔗 Outbound link → `outbound_click`
- 🎯 `data-ta-event` attribute

**Manual:**
```javascript
trackEvent('purchase', {amount: 99, currency: 'USD'})
```

**Files:**
- 🎨 `static/tracking.js` → `window.trackEvent()`
- 🐍 `analytics/views.py` → `track_event_view()`
- 💾 `analytics/models.py` → `Event`

### 📌 5. Public API

```
[External Tool]
      ↓
[Authorization: Api-Key <key>]
      ↓
[APIKeyAuthentication validate]
      ↓
[View returns JSON data]
```

**Files:**
- 🔑 `analytics/api/authentication.py`
- 🐍 `analytics/api/views.py`
- 💾 `websites/models.py` → `APIKey`

---

## 🔗 Important URLs

<details>
<summary><b>👤 User Pages</b></summary>

| URL | Description |
|-----|-------------|
| `/` | Dashboard home |
| `/accounts/register/` | Registration |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/accounts/profile/` | User profile |

</details>

<details>
<summary><b>🌐 Website Management</b></summary>

| URL | Description |
|-----|-------------|
| `/websites/` | All websites |
| `/websites/add/` | Add new website |
| `/websites/<id>/` | Single analytics |
| `/websites/<id>/events/` | Events dashboard |
| `/websites/<id>/map/` | Live world map |
| `/websites/<id>/email-settings/` | Email config |

</details>

<details>
<summary><b>📥 Export</b></summary>

| URL | Downloads |
|-----|-----------|
| `/websites/<id>/export/pageviews.csv` | Page views data |
| `/websites/<id>/export/visitors.csv` | Visitor data |
| `/websites/<id>/export/stats.csv` | Aggregated stats |

</details>

<details>
<summary><b>🔌 API Endpoints</b></summary>

| Method | URL | Purpose |
|--------|-----|---------|
| `POST` | `/api/track/` | Page view tracking |
| `POST` | `/api/track/event/` | Custom event |
| `GET` | `/api/stats/` | User stats |
| `GET` | `/api/realtime/` | Real-time data |
| `GET` | `/api/v1/websites/` | Public API list |
| `GET` | `/api/v1/websites/<id>/stats/` | Public API stats |
| `GET` | `/api/v1/websites/<id>/realtime/` | Public API realtime |

</details>

---

## 🔑 API Usage Examples

### 🐚 cURL

```bash
curl -H "Authorization: Api-Key YOUR_KEY" \
  http://127.0.0.1:8000/api/v1/websites/1/stats/
```

### 🐍 Python

```python
import requests

API_KEY = "your_api_key_here"
BASE = "http://127.0.0.1:8000/api/v1"
headers = {"Authorization": f"Api-Key {API_KEY}"}

r = requests.get(f"{BASE}/websites/1/stats/", headers=headers)
data = r.json()

print(f"📊 Total Views: {data['totals']['page_views']}")
print(f"👥 Visitors: {data['totals']['unique_visitors']}")
print(f"🌍 Top Countries: {data['countries'][:3]}")
```

### 🌐 JavaScript

```javascript
fetch('http://127.0.0.1:8000/api/v1/websites/1/stats/', {
    headers: { 
        'Authorization': 'Api-Key YOUR_KEY' 
    }
})
.then(r => r.json())
.then(data => {
    console.log(`Views: ${data.totals.page_views}`);
});
```

---

## 🎨 How to Track a Website

### Step 1️⃣ — Add Website

```
Login → Sidebar → Websites → "+ Add Website"
```

- **Name:** My Blog
- **Domain:** https://myblog.com

### Step 2️⃣ — Get Tracking Code

Website detail page এ **📋 Tracking Code** section এ যান।

```html
<script 
    src="http://yoursite.com/static/tracking.js" 
    data-tracking-id="YOUR-UNIQUE-ID">
</script>
```

### Step 3️⃣ — Paste on Your Website

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
    
    <!-- Traffic Analyzer -->
    <script 
        src="http://yoursite.com/static/tracking.js" 
        data-tracking-id="YOUR-TRACKING-ID">
    </script>
</head>
<body>
    ...
</body>
</html>
```

### Step 4️⃣ — Test

1. আপনার website visit করুন
2. Dashboard এ ফিরে আসুন
3. **"Active Now" count = 1** দেখাবে ✅
4. **Live Map** এ position দেখা যাবে 🌍

### 🎁 Bonus — Custom Events

```html
<button onclick="trackEvent('signup_click', {source: 'header'})">
    Sign Up
</button>

<button data-ta-event="buy_now">Buy Now</button>

<script>
trackEvent('purchase', {
    amount: 99,
    currency: 'USD',
    product: 'Pro Plan'
});
</script>
```

---

## 🔧 Common Commands

```bash
# 🚀 Server চালু
python manage.py runserver

# 🗄️ Migrations
python manage.py makemigrations
python manage.py migrate

# 👤 Superuser তৈরি
python manage.py createsuperuser

# 🎨 Static files collect
python manage.py collectstatic --noinput

# 🐚 Django shell
python manage.py shell

# ✅ System check
python manage.py check

# ⚡ Celery worker
celery -A config worker -l info --pool=solo

# ⏰ Celery beat
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# 🔴 Redis test
memurai-cli ping
```

---

## 🐛 Troubleshooting

<details>
<summary><b>❌ No module named 'X'</b></summary>

```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><b>❌ Connection refused (Redis)</b></summary>

Check: `memurai-cli ping`

Fix: Services.msc → Memurai → Start
</details>

<details>
<summary><b>❌ Port 8000 already in use</b></summary>

```bash
python manage.py runserver 8001
```
</details>

<details>
<summary><b>❌ Charts show হচ্ছে না</b></summary>

- Browser F12 → Console → error দেখুন
- Internet connection (Chart.js CDN)
- `Ctrl + Shift + R` hard refresh
</details>

<details>
<summary><b>❌ Email send হচ্ছে না</b></summary>

- `.env` এ Gmail credentials সঠিক?
- **App Password** ব্যবহার করেছেন?
- Celery worker running?
</details>

<details>
<summary><b>❌ Real-time count 0 দেখাচ্ছে</b></summary>

- Memurai running? (`memurai-cli ping` → PONG)
- Tracking script website এ installed?
- F12 → Network → `/api/track/` call হচ্ছে?
</details>

<details>
<summary><b>❌ Static files load হচ্ছে না</b></summary>

```bash
python manage.py collectstatic --clear --noinput
```
তারপর browser এ `Ctrl + Shift + R`
</details>

<details>
<summary><b>❌ Celery worker Windows এ crash</b></summary>

`--pool=solo` flag যোগ করুন:
```bash
celery -A config worker -l info --pool=solo
```
</details>

---

## 🔒 Security Best Practices

- 🔐 `.env` file Git এ commit করবেন না
- 🚫 Production এ `DEBUG=False` রাখুন
- 🔑 Strong `SECRET_KEY` ব্যবহার করুন
- 🌐 Specific `ALLOWED_HOSTS` দিন
- 🔒 HTTPS enable করুন
- 📧 Gmail App Password use করুন
- 🔄 API keys নিয়মিত rotate করুন
- 📊 Regular backup নিন

---

## 📊 Feature Status

| Feature | Status | Files |
|---------|:------:|-------|
| 🔐 User Authentication | ✅ | `accounts/` |
| 🌐 Website Management | ✅ | `websites/` |
| 🖱️ Page Tracking | ✅ | `tracking.js`, `analytics/` |
| ⚡ Real-time Visitors | ✅ | `analytics/realtime.py` |
| 🌍 GeoIP Location | ✅ | `analytics/country_coords.py` |
| 🎯 Custom Events | ✅ | `analytics/models.py` |
| 📥 CSV Export | ✅ | `websites/views.py` |
| 📧 Email Reports | ✅ | `websites/tasks.py` |
| 🔌 Public API | ✅ | `analytics/api/` |
| 🗺️ Live World Map | ✅ | `website_map.html` |
| 🌙 Dark Mode | ✅ | `main.css`, `main.js` |
| 📱 Responsive UI | ✅ | All templates |

---

## 🎓 Learning Resources

| Topic | Link |
|-------|------|
| 🐍 **Django** | [docs.djangoproject.com](https://docs.djangoproject.com/) |
| 🔌 **DRF** | [django-rest-framework.org](https://www.django-rest-framework.org/) |
| ⚡ **Celery** | [docs.celeryq.dev](https://docs.celeryq.dev/) |
| 📊 **Chart.js** | [chartjs.org](https://www.chartjs.org/) |
| 🗺️ **Leaflet** | [leafletjs.com](https://leafletjs.com/) |
| 🎨 **Bootstrap 5** | [getbootstrap.com](https://getbootstrap.com/) |

---

## 🚀 Future Roadmap

- [ ] 🎯 Funnel Analysis
- [ ] 📄 PDF Reports
- [ ] 🌐 Custom Domains
- [ ] 👥 Team Collaboration
- [ ] 🔔 Webhooks
- [ ] 📱 Mobile App
- [ ] 🔐 2FA

---

## 🤝 Contributing

1. 🍴 Fork করুন
2. 🌿 Branch বানান (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit করুন (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push করুন (`git push origin feature/AmazingFeature`)
5. 🎉 Pull Request খুলুন

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

<div align="center">

**Ratul Hasan**

[![GitHub](https://img.shields.io/badge/GitHub-@ratuuulhasan-181717?style=for-the-badge&logo=github)](https://github.com/ratuuulhasan)
[![Email](https://img.shields.io/badge/Email-hratul838@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hratul838@gmail.com)

*Built with ❤️ using Django*

</div>

---

<div align="center">

### ⭐ এই Project ভালো লাগলে Star দিন!

**Made with ❤️ in Bangladesh 🇧🇩**

[⬆️ Back to Top](#-traffic-analyzer)

</div>