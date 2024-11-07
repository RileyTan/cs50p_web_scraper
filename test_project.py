from project import pinpoint_table, save_html_as_dictionary, save_to_csv
import requests
from bs4 import BeautifulSoup
import pytest
import csv

@pytest.fixture
def soup():
    page = requests.get("https://en.wikipedia.org/wiki/List_of_highest-grossing_films")
    soup = BeautifulSoup(page.text, "lxml")

    return soup

def test_pinpoint_table(soup, monkeypatch):
    """
    this test function takes into consideration that pinpoint_table() takes in user input
    """

    # both cases of user inputting HTML and not doing so
    test_cases = [
        ["Yes", "wikitable sortable plainrowheaders sticky-header col4right col5center col6center", "0"],
        ["No", "Avengers: Endgame, Avatar: The Way of Water, Titanic"]
    ]

    for inputs in test_cases:
        inputs_iter = iter(inputs) # an iterator helps go through items in a list one by one, w/o storing all items at once. # lists and dictionaries are _iterables_, this is an _iterator_
        monkeypatch.setattr('builtins.input', lambda _: next(inputs_iter)) # simulates user input. returns the next item from inputs_iter each time input is called. input() is a built-in function in Python within the builtins module, hence the name 'builtins'

        table = pinpoint_table(soup)
        assert table is not None, "get_table() did not return a table"
        assert table.name == "table", "the BeautifulSoup Tag object's name is incorrect" # chewcks if BeautifuSoup object table is indeed an HTML <table> element

        table_text = table.get_text()
        assert "Avatar: The Way of Water" in table_text, "The table does not contain 'Avatar: The Way of Water'"

def test_save_html_as_dictionary(soup):
    """
    test whether output is a dictionary
    """
    table = soup.find("table", class_="wikitable sortable plainrowheaders sticky-header col4right col5center col6center")

    table_content = save_html_as_dictionary(table)
    assert isinstance(table_content, list), "get_table_content() should return us a list of dictionaries" # isinstance() lets us confirm the nature of variables, whether its an instance of a specific type or class
    assert len(table_content) > 0

    first_row = table_content[0]
    assert isinstance(first_row, dict), "first item in list should be dictionary"

    expected_keys = ["Rank", "Peak", "Title", "Worldwide gross", "Year", "Ref"]
    for key in expected_keys:
        assert key in first_row

    assert first_row["Title"] == "Avatar"

def test_save_to_csv():
    """
    converts list of dictionaries to csv file
    """
    results = [
        {"Title" : "Avatar", "Year":"2009"},
        {"Title" : "Avengers: Endgame", "Year":"2019"}
    ]

    test_filename = "test_output.csv"

    # writes the file
    save_to_csv(results, test_filename)

    # reads the file to confirm that it is written properly
    with open(test_filename, 'r') as file:
        reader = csv.DictReader(file) 
        rows = list(reader) # converts iterator of dictionaries to list of dictionaries

    assert rows == results

