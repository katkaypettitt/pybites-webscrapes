from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup

out_dir = "/tmp"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
# source:
# https://www.digminecraft.com/lists/enchantment_list_pc.php
URL = ("https://bites-data.s3.us-east-2.amazonaws.com/"
       "minecraft-enchantment.html")


class Enchantment:
    """Minecraft enchantment class

    Implements the following:
        id_name, name, max_level, description, items
    """

    pass


class Item:
    """Minecraft enchantable item class

    Implements the following:
        name, enchantments
    """
    pass


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

    # TODO: make enchantment class
    # TODO: finish this function 



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

"""
Armor: 
  [1] binding_curse
  [4] blast_protection
  [4] fire_protection
  [4] projectile_protection
  [4] protection
  [3] thorns 

Axe: 
  [5] bane_of_arthropods
  [5] efficiency
  [3] fortune
  [5] sharpness
  [1] silk_touch
  [5] smite 

Boots: 
  [3] depth_strider
  [4] feather_falling
  [2] frost_walker 

Bow: 
  [1] flame
  [1] infinity
  [5] power
  [2] punch 

Chestplate: 
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Crossbow: 
  [1] multishot
  [4] piercing
  [3] quick_charge 

Fishing Rod: 
  [3] luck_of_the_sea
  [3] lure
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Helmet: 
  [1] aqua_affinity
  [3] respiration 

Pickaxe: 
  [5] efficiency
  [3] fortune
  [1] mending
  [1] silk_touch
  [3] unbreaking
  [1] vanishing_curse 

Shovel: 
  [5] efficiency
  [3] fortune
  [1] silk_touch 

Sword: 
  [5] bane_of_arthropods
  [2] fire_aspect
  [2] knockback
  [3] looting
  [1] mending
  [5] sharpness
  [5] smite
  [3] sweeping
  [3] unbreaking
  [1] vanishing_curse 

Trident: 
  [1] channeling
  [5] impaling
  [3] loyalty
  [3] riptide
"""

