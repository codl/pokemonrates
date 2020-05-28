import httpx
from bs4 import BeautifulSoup
import re
import sys

URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
HEADER = re.compile("\s*Pokémon\s*")

with httpx.Client(
    headers={"user-agent": "Pokemon Rates +https://botsin.space/@pokemonrates"}
) as client:
    resp = client.get(URL)
    resp.raise_for_status()
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

print("\n".join(species_names))
print(
    "Written {} species to stdout\nTa-ta for now!".format(len(species_names)),
    file=sys.stderr,
)
