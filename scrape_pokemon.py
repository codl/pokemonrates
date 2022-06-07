import requests
from bs4 import BeautifulSoup
import re
import sys
import time

URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
HEADER = re.compile("\s*Pokémon\s*")

class AttemptsExceeded(Exception):
    pass

def fetch(attempts:int=6, verbose:bool=True) -> requests.Response:
    resp = None
    attempt = 0
    while not resp and attempt < attempts:
        try:
            resp = requests.get(URL, headers={"user-agent": "Pokemon Rates +https://botsin.space/@pokemonrates"})
            resp.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError) as e:
            resp = None
            delay = 10 ** attempt
            if verbose:
                print("Can't reach bulbapedia: {}\nRetrying in {} seconds...".format(
                    e, delay
                    )
                        , file=sys.stderr)
            time.sleep(delay)
            attempt += 1

    if resp:
        return resp
    else:
        raise AttemptsExceeded()

def parse_list(resp:requests.Response) -> list[str]:
    soup = BeautifulSoup(resp.text, "html.parser")

    species_names = []
    known = set()

    for table in soup.find_all("table"):
        th = table.find("th", string=HEADER)
        if not th:
            continue
        for i, element in enumerate(th.parent.find_all(True, recursive=False)):
            if element == th:
                header_index = i
        for tr in table.find_all("tr"):
            if tr == th.parent:
                continue
            species = tr.find_all(True, recursive=False)[header_index]
            name = "".join(species.stripped_strings)
            if name not in known:
                species_names.append(name)
                known.add(name)

    return species_names

if __name__ == '__main__':
    species_names = parse_list(fetch())
    print("\n".join(species_names))
    print(
        "Written {} species to stdout\nTa-ta for now!".format(len(species_names)),
        file=sys.stderr,
)
