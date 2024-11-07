import requests
from bs4 import BeautifulSoup
import csv

def main():
    url = input("URL: ")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "lxml")

    interested_table = pinpoint_table(soup)

    if interested_table:
        results = save_html_as_dictionary(interested_table)
        filename = input("Desired name of file: ")
        save_to_csv(results, filename)
        print("CSV has been generated")

    else:
        print("Table/table data not found")

def pinpoint_table(soup):
    """
    this function allows the user to choose between inspecting the source code or not.
    either ways, a BeautifulSoup Tag object will be returned
    """

    knowledge_of_html = input("Are you willing to inspect the source code? Yes/No: ").strip().lower()
    if knowledge_of_html == "yes":
        class_name = input("What is the table's class? ").strip()
        tables = soup.find_all('table', class_=class_name)
        table_index = int(input("What is the index of the table, indexing from 0: "))
        if 0 <= table_index < len(tables):
            table = tables[table_index]
            return table
        else:
            print("Can't find the table")
            return None
    else:
        tables = soup.find_all('table')
        stuff_seen = input("input content from your interested table: ")
        words = [word.strip() for word in stuff_seen.split(',')]

        max_match = 0
        best_match_table = None

        # loop through tables until i find
        for table in tables:
            table_text = table.get_text()
            match_count = sum(1 for word in words if word in table_text)

            if match_count > max_match:
                # with each loop, the max_matches and best_match_table changes only if the current table trumps the max_match
                max_match = match_count
                best_match_table = table

        # account for the case where match_count is never > 0, ie no matches
        if best_match_table:
            print("\nthere is a match\n")
            return best_match_table
        else:
            print("Please make sure your input text is separated by just a comma")
            return None


def save_html_as_dictionary(interested_table):
    """
    this function goes through the HTML and returns us the table
    within the <tbody>, retrieve all the rows, assuming that the first row <tr> consist of <th>, making these our dictionary keys
    and subsequent rows <tr> consist of <td>/<th>, making these our table data
    """
    table_body = interested_table.find_all("tr")

    headers_keys = [header.get_text(strip=True) for header in table_body[0].find_all("th")]
    # for each row
    # created a new dictionary
    # loop through each <td>, each <td> should be attached to each key
    # each row-dictionary is appended to our main list initialised up outside loop
    # we end up with a list of dictionaries
    table_data = []
    rows = table_body[1:]
    for row in rows:
        each_row = {}
        all_td = row.find_all(['td', 'th']) # note that some rows contain <th> and <td>
        for i, data in enumerate(all_td):
            cell = data.get_text(strip=True)
            each_row[headers_keys[i]] = cell
        table_data.append(each_row)

    return table_data

def save_to_csv(results, filename):
    """
    this function converts the results which is a list of dictionaries into a
    chosen filename, assuming that it is a CSV file
    """
    if not results:
        return

    headers = results[0].keys()
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


if __name__ == "__main__":
    main()



