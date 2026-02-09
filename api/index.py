from fastapi import FastAPI, Query, HTTPException
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = FastAPI()

@app.get("/scrape")
def scrape_images(url: str = Query(..., description="URL to scrape")):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    soup = BeautifulSoup(response.text, "html.parser")

    allowed_ext = (".jpg", ".jpeg")
    seen = set()
    images = []

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        full_url = urljoin(url, src)

        # ignore query params
        path = urlparse(full_url).path.lower()

        if path.endswith(allowed_ext):
            if full_url not in seen:
                seen.add(full_url)
                images.append(full_url)

    return {
        "count": len(images),
        "images": images
    }
