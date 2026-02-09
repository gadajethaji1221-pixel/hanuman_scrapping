import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def handler(request):
    # Get URL from query parameter
    url = request.args.get("url")

    if not url:
        return {
            "statusCode": 400,
            "body": "Missing ?url= parameter"
        }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        images = []

        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                full_url = urljoin(url, src)
                images.append(full_url)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": str(images)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
