from collections import defaultdict
from dataclasses import dataclass, field
from functools import total_ordering
from pathlib import Path
from re import compile, search
from typing import Any, DefaultDict, List
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup

out_dir = "/tmp"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
# source:
# https://www.digminecraft.com/lists/enchantment_list_pc.php
URL = ("https://bites-data.s3.us-east-2.amazonaws.com/"
       "minecraft-enchantment.html")


#################### CLASSES ####################

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

@dataclass
class Item:
    """Minecraft enchantable item class

    Implements the following:
        name, enchantments
    """
    name: str
    enchantments: List[Enchantment] = field(default_factory=list)

    def __str__(self):
        enchants = sorted(self.enchantments)
        enc_list = [f"\n  [{enc.max_level}] {enc.id_name}" for enc in enchants]
        return f"{self.name.title()}: {''.join(enc_list)}"
       
       
 #################### FUNCTIONS ####################

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

# TODO: Finish this function
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


# TODO: Finish this function
def generate_items(data):
    """Generates a dictionary of Item objects

    With the key being the item name.
    """
    pass


#################### HELPER FUNCTIONS ####################

def parse_html(soup):
    """Parses BeautifulSoup object and returns the table

    :param soup: BeautifulSoup object
    :return: List of the rows that make up the table
    """
    table = soup.find("table", {"id": "minecraft_items"})
    data = [
        [td.get_text() for td in row.find_all("td")] for row in table.find_all("tr")
    ]

    return data[1:]


def gen_item_set(data):
    """Returns a set of item names

    :param data: Dictionary of Enchantment objects
    :return: Set of sorted item object name strings
    """
    mc_items = set()
    for enchantment in data.keys():
        for item in data[enchantment].items:
            mc_items.add(item)

    return sorted(mc_items)


def split_title(title):
    """
    Splits the title string

    :param title: String of the enchantment title
    :return: Tuple(id_names, names)
    """
    pattern = compile(r"(.*)\((.*)\)")
    names, id_names = search(pattern, title).groups()
    return id_names, names


def clean_up_names(item_names):
    """Cleans up item names

    :param item_names: String of item names
    :return: String of cleaned up item names
    """
    unwanted = (".png", "_sm", "iron_", "enchanted_")

    if "fishing_rod" in item_names:
        item_names = item_names.replace("fishing_rod", "fishingrod")

    for chars in unwanted:
        if chars in item_names:
            item_names = item_names.replace(chars, "")

    item_names = item_names.split("_")
    item_names = [
        "fishing_rod" if item == "fishingrod" else item for item in item_names
    ]

    return " ".join(item_names)


def enchantable_items(soup):
    """Scrapes BeautifulSoup object for items

    :param soup: BeautifulSoup object
    :return: List of enchantable items lists
    """
    table = soup.find("table", {"id": "minecraft_items"})
    items = [
        clean_up_names(img["data-src"].split("/")[-1]).split()
        for img in table.find_all("img")
    ]

    return items


#################### MAIN FUNCTION ####################

def main():
    """This function is here to help you test your final code.

    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    # TODO: Uncomment once generate item function is working
    # for item in minecraft_items:
    #     print(minecraft_items[item], "\n")


if __name__ == "__main__":
    main()
