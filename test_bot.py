import pytest
from run import pokémon_from_status_content


all_pokémon = ("pikachu", "snorlax", "slither wing", "abra")


pokémon_from_status_content_test_cases = (
    ("", set()),
    ("patamon", set()),
    ("pikachu", {"pikachu"}),
    (
        "<p><b>pikachu</b></p>",
        {
            "pikachu",
        },
    ),
    (
        "<p><b>pika</b>chu</p>",
        {
            "pikachu",
        },
    ),
    ("pikachu snorlax", {"pikachu", "snorlax"}),
    ("<a href=pikachu></a>", set()),
    (
        "PiKaChU",
        {
            "pikachu",
        },
    ),
    (
        "slither wing",
        {
            "slither wing",
        },
    ),
    (
        "pikachu slither wing",
        {
            "pikachu",
            "slither wing",
        },
    ),
    ("my dog is a labrador", set()),
)


@pytest.mark.parametrize("test_input,expected", pokémon_from_status_content_test_cases)
def test_pokémon_from_status_content(test_input, expected):
    assert pokémon_from_status_content(test_input, all_pokémon) == expected
