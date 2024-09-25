import requests
from bs4 import BeautifulSoup
import re
import sys
import time

URL = "https://bulbapedia.bulbagarden.net/w/api.php?action=parse&page=List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number&prop=text&format=json"
HEADER = re.compile(r"\s*Pokémon\s*")
POKEMON_PAGE_TITLE = re.compile(r".*\s+\(Pokémon\)\s*$")


class AttemptsExceeded(Exception):
    pass


def fetch(attempts: int = 6, verbose: bool = True) -> requests.Response:
    resp = None
    attempt = 0
    while not resp and attempt < attempts:
        try:
            resp = requests.get(
                URL,
                headers={
                    "user-agent": "Pokemon Rates +https://botsin.space/@pokemonrates"
                },
            )
            resp.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError) as e:
            resp = None
            delay = 10**attempt
            if verbose:
                print(
                    "Can't reach bulbapedia: {}\nRetrying in {} seconds...".format(
                        e, delay
                    ),
                    file=sys.stderr,
                )
            time.sleep(delay)
            attempt += 1

    if resp:
        return resp
    else:
        raise AttemptsExceeded()


def extract_html_from_response(resp: requests.Response) -> str:
    d = resp.json()
    html = d["parse"]["text"]["*"]
    return html


def parse_list(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    species_names = []
    known = set()

    for table in soup.find_all("table"):
        th = table.find("th", string=HEADER)
        if not th:
            continue
        species_all = table.find_all("a", title=POKEMON_PAGE_TITLE)
        for species in species_all:
            name = "".join(species.stripped_strings)
            if name not in known:
                species_names.append(name)
                known.add(name)

    return species_names


if __name__ == "__main__":
    resp = fetch()
    html = extract_html_from_response(resp)
    species_names = parse_list(html)
    print("\n".join(sorted(species_names)))
    print(
        "Written {} species to stdout\nTa-ta for now!".format(len(species_names)),
        file=sys.stderr,
    )
