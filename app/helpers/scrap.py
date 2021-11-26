import bs4
import requests
from typing import Dict


def scrap(url: str) -> bs4.BeautifulSoup:
    resp: requests.Response = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    return soup


BODY_DIV_CONTENT: str = 'body div[id="content"]'


def get_name(soup: bs4.BeautifulSoup) -> str:
    div: bs4.ResultSet[bs4.Tag] = soup.select(
        f'{BODY_DIV_CONTENT} h1[id="firstHeading"] i'
    )
    name = div[0].text
    print(name)
    return name


DIV_CONTENT_TABLE: str = (
    BODY_DIV_CONTENT
    + ' div[id="bodyContent"]'
    + ' div[id="mw-content-text"]'
    + ' div[class="mw-parser-output"]'
    + ' table[class="infobox biota"]'
    + " tbody"
)


def get_temporal_range(soup: bs4.BeautifulSoup) -> str:
    div = f"{DIV_CONTENT_TABLE} tr th div"
    a: bs4.ResultSet[bs4.Tag] = soup.select_one(div + " a")
    spans: bs4.ResultSet[bs4.Tag] = soup.select(div + ' span[class="noprint"] span')
    span_time: str = ""
    for span in spans:
        span_time += span.text if span.text else ""
    print(f"{a.text} ({span_time})")
    return f"{a.text} ({span_time})"


def get_data(dinosaur_name: str) -> Dict:
    dinosaur_data: Dict = {}
    url: str = f"https://en.wikipedia.org/wiki/{dinosaur_name}"
    soup: bs4.BeautifulSoup = scrap(url)
    dinosaur_data["name"] = get_name(soup)
    dinosaur_data["temporalRange"] = get_temporal_range(soup)
    return dinosaur_data
