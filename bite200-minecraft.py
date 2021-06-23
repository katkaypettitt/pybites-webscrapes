from pathlib import Path
from urllib.request import urlretrieve
from dataclasses import dataclass, field
from functools import total_ordering

from bs4 import BeautifulSoup as Soup

out_dir = "/tmp"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
# source:
# https://www.digminecraft.com/lists/enchantment_list_pc.php
URL = ("https://bites-data.s3.us-east-2.amazonaws.com/"
       "minecraft-enchantment.html")

@dataclass
@total_ordering
class Enchantment:
    """Minecraft enchantment class

    Implements the following:
        id_name, name, max_level, description, items
    """
    id_name: str
    name: str
    max_level: int
    description: str
    items: List[str] = field(default_factory=list)

    def __str__(self):
        return f"{self.name} ({self.max_level}): {self.description}"

    def __lt__(self, other):
        return self.id_name < other.id_name


class Item:
    """Minecraft enchantable item class

    Implements the following:
        name, enchantments
    """
    def __int__(self, name):
        self.name = name

    def __str__(self):
        return Enchantment(self.name)


def generate_enchantments(soup):
    """Generates a dictionary of Enchantment objects

    With the key being the id_name of the enchantment.
    """
    right_table = soup.select('table#minecraft_items td')

    id_name_list = []
    name_list = []
    maxlevel_list = []
    description_list = []
    minecraft_id_list = []
    items_list = []
    version_list = []

    row_length = 6
    row_number = 0
    for row in right_table:
        if row_number == row_length:
            row_number = 0
        if row_number == 0:  # names and id names
            name_list.append(row.get_text().split('(')[0])
            id_name_list.append(row.get_text().split('(')[1][:-1])
        if row_number == 1:  # max levels
            maxlevel_list.append(row.get_text())
        if row_number == 2:  # descriptions
            description_list.append(row.get_text())
        if row_number == 3:  # ids
            minecraft_id_list.append(row.get_text())
        if row_number == 4:  # item information
            items_list.append(row.get_text())
        if row_number == 5:  # version
            version_list.append(row.get_text())
        row_number += 1


def generate_items(data):
    """Generates a dictionary of Item objects

    With the key being the item name.
    """
    pass


def get_soup(file=HTML_FILE):
    """Retrieves/takes source HTML and returns a BeautifulSoup object"""
    if isinstance(file, Path):
        if not HTML_FILE.is_file():
            urlretrieve(URL, HTML_FILE)

        with file.open() as html_source:
            soup = Soup(html_source, "html.parser")
    else:
        soup = Soup(file, "html.parser")

    return soup


def main():
    """This function is here to help you test your final code.

    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    # for item in minecraft_items:
    #     print(minecraft_items[item], "\n")


if __name__ == "__main__":
    main()
