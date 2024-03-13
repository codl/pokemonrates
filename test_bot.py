import pytest
from run import pokémon_from_status_content


all_pokémon = ("pikachu", "snorlax", "slither wing")


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
        pytest.param(
            "Slither Wing",
            {
                "slither wing",
            },
            marks=pytest.mark.xfail,
        ),
        pytest.param(
            "pikachu slither wing",
            {
                "pikachu",
                "slither wing",
            },
            marks=pytest.mark.xfail,
        ),
    ),
)
def test_pokémon_from_status_content(test_input, expected):
    assert pokémon_from_status_content(test_input, all_pokémon) == expected
