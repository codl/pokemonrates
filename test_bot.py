import pytest
from run import pokémon_from_status_content


all_pokémon = ("pikachu", "snorlax", "slither wing", "abra")


@pytest.mark.parametrize(
    "test_input,expected",
    (
        ("", set()),
        ("patamon", set()),
        ("pikachu", {"pikachu"}),
        (
            "<p><b>pikachu</b></p>",
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
            "Slither Wing",
            {
                "slither wing",
            }
        ),
        (
            "pikachu slither wing",
            {
                "pikachu",
                "slither wing",
            }
        ),
        pytest.param("my dog is a labrador", set(), marks=pytest.mark.xfail),
    ),
)
def test_pokémon_from_status_content(test_input, expected):
    assert pokémon_from_status_content(test_input, all_pokémon) == expected
