import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

def handler(request):
    # Target URL (hardcoded since you said function only)
    URL = "https://salangpurhanumanji.org/dev-darshan/dev-darshan-detail/dev-darshan.php?date=2026-01-28"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        allowed_ext = (".jpg", ".jpeg")
        seen = set()
        images = []

        for img in soup.find_all("img"):
            src = img.get("src")
            if not src:
                continue

            full_url = urljoin(URL, src)

            path = urlparse(full_url).path.lower()
            if path.endswith(allowed_ext):
                if full_url not in seen:
                    seen.add(full_url)
                    images.append(full_url)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(images)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
