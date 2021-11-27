import bs4
import requests
from typing import Dict, List


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
    return f"{a.text} ({span_time})".replace("\xa0", " ")


def get_species(tag: bs4.Tag) -> str:
    b: bs4.ResultSet[bs4.Tag] = tag.select("i b")
    if b:
        return b[0].text.strip()

    i: bs4.ResultSet[bs4.Tag] = tag.select("b span i")
    if i:
        return i[0].text.strip()


def get_scientific_classification(soup: bs4.BeautifulSoup, classification: str) -> str:
    trs: bs4.ResultSet[bs4.Tag] = soup.select(f"{DIV_CONTENT_TABLE} tr")
    matches: List[str] = []
    for tr in trs:
        tds: bs4.ResultSet[bs4.Tag] = tr.select("td")
        if len(tds) == 2 and classification != "species":
            if tds[0].text.strip() == classification.capitalize() + ":":
                a = tds[1].select("a")
                # print(tds[0].text.strip(), a[0].text)
                matches.append(a[0].text.strip())
        elif len(tds) == 1 and classification == "species":
            species: str = get_species(tds[0])
            if species:
                matches.append(species)
        else:
            continue

    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        return matches


def get_data(dinosaur_name: str) -> Dict:
    dinosaur_data: Dict = {}
    url: str = f"https://en.wikipedia.org/wiki/{dinosaur_name}"
    soup: bs4.BeautifulSoup = scrap(url)
    dinosaur_data["name"] = get_name(soup)
    dinosaur_data["temporalRange"] = get_temporal_range(soup)
    dinosaur_data["kingdom"] = get_scientific_classification(soup, "kingdom")
    dinosaur_data["phylum"] = get_scientific_classification(soup, "phylum")
    dinosaur_data["clade"] = get_scientific_classification(soup, "clade")
    dinosaur_data["family"] = get_scientific_classification(soup, "family")
    dinosaur_data["subfamily"] = get_scientific_classification(soup, "subfamily")
    dinosaur_data["genus"] = get_scientific_classification(soup, "genus")
    dinosaur_data["species"] = get_scientific_classification(soup, "species")
    print(dinosaur_data)
    return dinosaur_data
