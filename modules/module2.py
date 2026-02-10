import urllib.robotparser as robotparser
from urllib.parse import urlparse
import requests

def checkRobotsTxt(url):
    # Check the robots.txt file for the given URL and return the parser
    origin = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    robots_url = f"{origin}/robots.txt"

    try:
        r = requests.get(robots_url, timeout=5, headers={"User-Agent": "MySimpleCrawler/1.0"})
        status = r.status_code
        text = r.text if status == 200 else ""
    except requests.RequestException:
        status = None
        text = ""

    rp = robotparser.RobotFileParser()
    # RobotFileParser.read() returns None; use parse() with the fetched lines instead
    if text:
        rp.parse(text.splitlines())
    else:
        rp.parse([])

    print(f"Robots.txt fetched from {robots_url} (status={status}):\n{text}")
    return rp

def robotsPermission(rp, url):
    # Check if the given path is allowed to be crawled according to the robots.txt rules
    path = urlparse(url).path or "/"
    if not rp.can_fetch("MySimpleCrawler/1.0", path):
        print("Blocked by robots.txt:", url)
    else:
        print("Allowed — proceed to fetch", url)
        return url