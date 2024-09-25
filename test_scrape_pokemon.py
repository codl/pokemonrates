from unittest.mock import MagicMock

import time
import requests
from scrape_pokemon import fetch, parse_list


def test_fetch(monkeypatch):
    monkeypatch.setattr(time, "sleep", MagicMock())
    resp = MagicMock()
    monkeypatch.setattr(
        requests,
        "get",
        MagicMock(side_effect=[requests.ConnectionError(), requests.HTTPError(), resp]),
    )

    assert resp is fetch()
    assert time.sleep.call_count == 2
    assert time.sleep.call_args_list[0] < time.sleep.call_args_list[1]


def test_parse_list():
    with open("test_data/scrape_input.html", "r") as f:
        html = f.read()
    with open("test_data/scrape_output.txt", "r") as f:
        expected = set(f.read().splitlines())

    assert set(parse_list(html)) == expected
