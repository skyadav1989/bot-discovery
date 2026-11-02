# Bot Discovery — Crawler Response Demo

A FastAPI app that returns **different tailored JSON payloads** based on the `User-Agent` of the requester.  
Compare how Browser, GPTBot, Googlebot, ClaudeBot, and PerplexityBot each see the same product endpoint — side-by-side.

## Live Demo

> Deploy your own on Render: see [Deploy to Render](#deploy-to-render) below.

## Supported Bots

| Bot | Colour | Response Style |
|---|---|---|
| 🌐 Browser | Blue | HTML page payload + UI hints |
| 🤖 GPTBot | Green | AI-readable summary + key features |
| 🔍 Googlebot | Amber | SEO metadata + Schema.org JSON-LD |
| 🧠 ClaudeBot | Purple | Conversational content + citation context |
| ⚡ PerplexityBot | Cyan | Answer snippet + related queries |

## Run Locally

```bash
# 1. Clone
git clone https://github.com/skyadav1989/bot-discovery.git
cd bot-discovery

# 2. Create virtual env (optional but recommended)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start server
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open http://127.0.0.1:8000

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Comparison UI |
| `GET` | `/product` | Returns payload based on actual incoming User-Agent |
| `GET` | `/api/test/{kind}` | Simulates a bot request (kind: `browser`, `gptbot`, `googlebot`, `claudebot`, `perplexitybot`) |

## Test with curl

```bash
# Browser
curl -A 'Mozilla/5.0 Chrome/130.0.0.0 Safari/537.36' http://localhost:8000/product

# GPTBot
curl -A 'Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)' http://localhost:8000/product

# Googlebot
curl -A 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' http://localhost:8000/product

# ClaudeBot
curl -A 'Mozilla/5.0 (compatible; ClaudeBot/1.0; +https://anthropic.com/claude-bot)' http://localhost:8000/product

# PerplexityBot
curl -A 'Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)' http://localhost:8000/product
```

---

## Deploy to Render

### Prerequisites
- A free account at [render.com](https://render.com)
- This repo pushed to GitHub

### Steps

#### 1. Push code to GitHub

```bash
git clone https://github.com/skyadav1989/bot-discovery.git   # or your fork
cd bot-discovery
# ... make changes ...
git add .
git commit -m "your message"
git push origin main
```

#### 2. Create a new Web Service on Render

1. Log in to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub account if not already connected
4. Select the `skyadav1989/bot-discovery` repository
5. Click **Connect**

#### 3. Configure the service

| Setting | Value |
|---|---|
| **Name** | `bot-discovery` (or any name) |
| **Region** | Closest to your users |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

> Render automatically injects the `$PORT` environment variable. The `render.yaml`
> file in this repo pre-fills these settings if you use **Blueprint** deployment.

#### 4. Deploy via Blueprint (one-click alternative)

1. Go to [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)
2. Click **New Blueprint Instance**
3. Select this repository — Render will read `render.yaml` and auto-configure everything
4. Click **Apply**

#### 5. Access your live URL

After the build completes (≈ 2 minutes), Render provides a URL like:

```
https://bot-discovery.onrender.com
```

> **Note:** Free-tier services spin down after 15 minutes of inactivity.  
> The first request after a cold start may take ~30 seconds.

---

## Important Security Note

User-Agent strings are trivially spoofable and must **not** be treated as proof of crawler identity.  
This is a **local demonstration only**. For production, verify crawler IPs using the operator''s  
published IP ranges or reverse/forward DNS verification.  
Keep facts consistent across user agents — avoid deceptive cloaking.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- Vanilla HTML / CSS / JS — frontend
