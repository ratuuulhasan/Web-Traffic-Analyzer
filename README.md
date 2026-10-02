# 📊 Traffic Analyzer

A self-hosted web analytics platform built with Django — track visitors, monitor real-time traffic, analyze behavior, and get automated reports. An open-source alternative to Google Analytics.

![Django](https://img.shields.io/badge/Django-5.x-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![Redis](https://img.shields.io/badge/Redis-Memurai-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 📈 Analytics
- **Page View Tracking** — JavaScript snippet দিয়ে কোনো website track করা যায়
- **Unique Visitor Detection** — Cookie-based visitor identification
- **Bounce Rate Calculation** — Single-page visits measure
- **Browser / OS / Device Breakdown** — User-agent parsing
- **Geographic Tracking** — GeoIP দিয়ে country detection

### ⚡ Real-time
- **Live Visitor Count** — Redis/Memurai powered real-time counter
- **Active Visitors Panel** — Currently on-site visitors এর live list
- **Live World Map** — Leaflet.js দিয়ে visitor দের geographic map
- **Auto-refresh** — প্রতি 5 seconds এ update

### 🎯 Advanced Tracking
- **Custom Events** — Button clicks, form submits, purchases track
- **Auto-tracking** — Form submits, outbound links স্বয়ংক্রিয়ভাবে track
- **Session Tracking** — Visitor দের session duration

### 📊 Reporting
- **Interactive Dashboard** — Chart.js দিয়ে beautiful charts
- **Per-Website Analytics** — প্রতিটা website এর আলাদা dashboard
- **CSV Export** — PageViews, Visitors, Stats download
- **Email Reports** — Daily/Weekly/Monthly automatic emails (Celery)

### 🔌 API
- **REST API with Token Auth** — External tools এর জন্য API
- **API Key per Website** — নিরাপদ per-website access
- **Rate Limiting** — 1000 requests/hour

### 🎨 UI
- **Dark Mode** — localStorage-supported theme toggle
- **Modern Sidebar** — Responsive, collapsible navigation
- **Toast Notifications** — Non-intrusive alerts
- **Number Animations** — Smooth count-up effects

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.x, Django REST Framework |
| **Database** | SQLite (dev) / PostgreSQL (production) |
| **Cache & Broker** | Redis (Memurai on Windows) |
| **Task Queue** | Celery + Celery Beat |
| **Frontend** | Bootstrap 5, Chart.js, Leaflet.js |
| **GeoIP** | MaxMind GeoLite2 |
| **Email** | SMTP (Gmail) |

---

## 🚀 Installation

### Prerequisites

- Python 3.11+
- Redis / Memurai (Windows এ)
- Git

### Step 1: Clone & Setup

```bash
git clone https://github.com/yourusername/traffic-analyzer.git
cd traffic-analyzer

# Virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate