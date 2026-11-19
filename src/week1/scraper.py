from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

# Standard headers to fetch a website
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def _render(url: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(user_agent=header["User-Agent"])
        page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        html = page.content()
        browser.close()
        return html


class Website:
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        try:
            response = requests.get(url, headers=header)
            self.soup = BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching website: {e}")
            self.soup = None

    def contents(self) -> str:
        if not self.soup:
            return ""
        title = self.soup.title.string if self.soup.title else "No title found"
        if self.soup.body:
            for irrelevant in self.soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = self.soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
        return (title + "\n\n" + text)[:2000]

    def links(self) -> list[str]:
        if not self.soup:
            return []
        links = [link.get("href") for link in self.soup.find_all("a")]
        return [link for link in links if link]
