import pytest
from run import pokémon_from_status_content


all_pokémon = ("Pikachu", "Snorlax", "Slither Wing", "Abra")


pokémon_from_status_content_test_cases = (
    ("", set()),
    ("patamon", set()),
    ("pikachu", {"Pikachu"}),
    (
        "<p><b>pikachu</b></p>",
        {
            "Pikachu",
        },
    ),
    (
        "<p><b>pika</b>chu</p>",
        {
            "Pikachu",
        },
    ),
    ("pikachu snorlax", {"Pikachu", "Snorlax"}),
    ("<a href=pikachu></a>", set()),
    (
        "PiKaChU",
        {
            "Pikachu",
        },
    ),
    (
        "slither wing",
        {
            "Slither Wing",
        },
    ),
    (
        "pikachu slither wing",
        {
            "Pikachu",
            "Slither Wing",
        },
    ),
    ("my dog is a labrador", set()),
)


@pytest.mark.parametrize("test_input,expected", pokémon_from_status_content_test_cases)
def test_pokémon_from_status_content(test_input, expected):
    assert pokémon_from_status_content(test_input, all_pokémon) == expected


def test_pokémon_from_status_content_regex():
    assert pokémon_from_status_content("MRA Mime", ("Mr. Mime",)) == set()
