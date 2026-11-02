from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Crawler Response Demo", version="1.0.0")

BOTS = {
    "gptbot": "GPTBot",
    "googlebot": "Googlebot",
    "claudebot": "ClaudeBot",
    "perplexitybot": "PerplexityBot",
    "browser": "Browser",
}

USER_AGENTS = {
    "browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36",
    "gptbot": "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)",
    "googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "claudebot": "Mozilla/5.0 (compatible; ClaudeBot/1.0; +https://anthropic.com/claude-bot)",
    "perplexitybot": "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
}

def classify_user_agent(user_agent: str) -> str:
    ua = (user_agent or "").lower()
    if "gptbot" in ua:
        return "gptbot"
    if "googlebot" in ua:
        return "googlebot"
    if "claudebot" in ua:
        return "claudebot"
    if "perplexitybot" in ua:
        return "perplexitybot"
    return "browser"

def build_response(kind: str) -> dict:
    common = {
        "product_id": "DEMO-1001",
        "product_name": "Smart LED Ceiling Light",
        "price": "₹2,499",
        "availability": "In Stock",
    }
    if kind == "gptbot":
        return {
            **common,
            "response_type": "GPTBOT_AI_SUMMARY",
            "content": (
                "The Smart LED Ceiling Light is an energy-efficient indoor lighting "
                "product with adjustable brightness. It costs ₹2,499 and is currently "
                "in stock. This is demonstration content for crawler testing."
            ),
            "key_features": [
                "Energy-efficient LED lighting",
                "Adjustable brightness",
                "Suitable for indoor use",
            ],
        }
    if kind == "googlebot":
        return {
            **common,
            "response_type": "GOOGLEBOT_SEARCH_CONTENT",
            "title": "Smart LED Ceiling Light | Demo Store",
            "meta_description": (
                "Shop the Smart LED Ceiling Light for efficient indoor illumination. "
                "Price ₹2,499. Currently in stock."
            ),
            "canonical_url": "https://demo.example.com/smart-led-ceiling-light",
            "structured_data": {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": common["product_name"],
                "sku": common["product_id"],
                "offers": {
                    "@type": "Offer",
                    "price": "2499",
                    "priceCurrency": "INR",
                    "availability": "https://schema.org/InStock",
                },
            },
        }
    if kind == "claudebot":
        return {
            **common,
            "response_type": "CLAUDEBOT_CONVERSATIONAL",
            "content": (
                "The Smart LED Ceiling Light (SKU: DEMO-1001) is a premium indoor "
                "lighting solution priced at ₹2,499. It features energy-efficient LEDs "
                "with adjustable brightness levels. Currently available in stock."
            ),
            "tone": "conversational",
            "citation_context": "Demo Store product listing — verified in stock as of demo date.",
            "key_facts": [
                "Price: ₹2,499 (INR)",
                "Status: In Stock",
                "Category: Indoor LED Lighting",
                "Feature: Adjustable Brightness",
            ],
        }
    if kind == "perplexitybot":
        return {
            **common,
            "response_type": "PERPLEXITYBOT_ANSWER_SNIPPET",
            "content": (
                "Smart LED Ceiling Light — ₹2,499, currently in stock at Demo Store. "
                "Energy-efficient LED with adjustable brightness for indoor use."
            ),
            "answer_snippet": "Smart LED Ceiling Light costs ₹2,499 and is in stock.",
            "source_url": "https://demo.example.com/smart-led-ceiling-light",
            "freshness": "real-time",
            "related_queries": [
                "Best LED ceiling lights India",
                "Energy efficient indoor lighting",
                "Smart lighting under ₹3000",
            ],
        }
    return {
        **common,
        "response_type": "BROWSER_HTML_PAGE",
        "content": (
            "Welcome to Demo Store. Explore the Smart LED Ceiling Light, "
            "check product details, and add it to your cart."
        ),
        "ui": ["Product image", "Quantity selector", "Add to cart button"],
    }

@app.get("/", response_class=HTMLResponse)
async def home():
    return (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/product")
async def product(request: Request):
    ua = request.headers.get("user-agent", "")
    kind = classify_user_agent(ua)
    payload = build_response(kind)
    payload["detected_as"] = BOTS[kind]
    payload["received_user_agent"] = ua
    return JSONResponse(payload, headers={"Vary": "User-Agent"})

@app.get("/api/test/{kind}")
async def fake_request(kind: str):
    kind = kind.lower()
    if kind not in USER_AGENTS:
        valid = ", ".join(USER_AGENTS.keys())
        return JSONResponse({"error": f"Unknown kind. Use one of: {valid}"}, status_code=400)

    # Call the classification + response logic directly (no HTTP self-call).
    # This is production-safe: avoids hardcoded host/port that would break on Render.
    ua = USER_AGENTS[kind]
    detected_kind = classify_user_agent(ua)
    payload = build_response(detected_kind)
    payload["detected_as"] = BOTS[detected_kind]
    payload["received_user_agent"] = ua

    return JSONResponse({
        "simulated_request": kind,
        "sent_user_agent": ua,
        "http_status": 200,
        "response": payload,
    })
