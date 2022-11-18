import os
import re
from enum import Enum

from markdownify import markdownify as md

from constants import *
from text_handling import Formatter

classes = [
    "Hero", 
    "Bandit", 
    "Astrologer", 
    "Warrior", 
    "Prisoner", 
    "Confessor", 
    "Wretch", 
    "Vagabond", 
    "Prophet", 
    "Samurai", 
]

stats = [
    "Stats", 
    "Vigor", 
    "Mind", 
    "Endurance", 
    "Strength", 
    "Dexterity", 
    "Intelligence", 
    "Faith", 
    "Arcane", 
    "Discovery", 
    "FP", 
    "Poise", 
    "Robustness", 
    "Standard Damage", 
    "Strike Damage", 
    "Critical Damage", 
]

status_effects = [
    "Buffs and Debuffs", 
    "Poison", 
    "Scarlet Rot", 
    "Blood Loss", 
    "Frostbite", 
    "Sleep", 
    "Madness", 
    "Death Blight", 
    "Hemorrhage", 
    "/Hemorrhage", 
]

spell_type = [
    "Sorceries", 
    "Bestial Incantations", 
    "Blood Incantations", 
    "Dragon Communion Incantations", 
    "Dragon Cult Incantations", 
    "Erdtree Incantations", 
    "Fire Giant Incantations", 
    "Fire Monk Incantations", 
    "Frenzied Flame Incantations", 
    "Godskin Apostle Incantations", 
    "Golden Order Incantations", 
    "Servants of Rot Incantations", 
    "Two Fingers Incantations", 
    #------------------------------
    "Incantations", 
    "Aberrant Sorceries", 
    "Carian Sorceries", 
    "Claymen Sorceries", 
    "Crystalian Sorceries", 
    "Death Sorceries", 
    "Full Moon Sorceries", 
    "Glintstone Sorceries", 
    "Gravity Sorceries", 
    "Loretta's Sorceries", 
    "Magma Sorceries", 
    "Night Sorceries", 
    "Primeval Sorceries", 
    "Cold Sorceries", 
]

weapon_type = [
    "Daggers", 
    "Straight Swords", 
    "Greatswords", 
    "Colossal Swords ", 
    "Thrusting Swords", 
    "Heavy Thrusting Swords", 
    "Curved Swords", 
    "Curved Greatswords", 
    "Katanas", 
    "Twinblades", 
    "Axes", 
    "Greataxes", 
    "Hammers", 
    "Flails", 
    "Great Hammers", 
    "Colossal Weapons", 
    "Spears", 
    "Great Spears", 
    "Halberds", 
    "Reapers", 
    "Whips", 
    "Fists", 
    "Claws", 
    "Light Bows", 
    "Bows", 
    "Greatbows", 
    "Crossbows", 
    "Ballistae", 
    "Glintstone Staffs", 
    "Sacred Seals", 
    "Torches", 
    "Tools", 
]

shield_type = [
    "Small Shields", 
    "Medium Shields", 
    "Greatshields", 
]

hide_list = [
    "Ashes of War", 
    "Consumables", 
    "Magic", 
    "Magic Spells", 
    "Runes", 
    "Skills", 
    "Smithing Stones", 
    "Somber Smithing Stones", 
    "Patch Notes", 
    "Creatures and Enemies", 
    "New Game Plus", 
    "Upgrades", 
    "Crafting Materials", 
    "Cookbooks", 
    "Builds", 
    "Parrying", 
    "Sites of Grace", 
]

# List of entities that exhibit parsing issues due to inconsistency with other similar pages
weapons_blacklist = ["Miquellan Knight's Sword", "Greataxe"]
items_blacklist = []
spells_blacklist = ["Placidusax's Ruin"]
bosses_blacklist = ["Dragonkin Soldier"]

# The Legacy Dungeons page is different enough, and there few enough instances, that these can be hardcoded here
legacy_dungeons = [
    "/Leyndell+Royal+Capital+(Legacy+Dungeon)", 
    "/Stormveil+Castle", 
    "/Raya+Lucaria+Academy",  
    "/Volcano+Manor", 
    "/Miquella's+Haligtree",
    "/Elphael,+Brace+of+the+Haligtree", 
    "/Crumbling+Farum+Azula", 
]

class EntityCategory(Enum):
    BOSSES = 'Bosses'
    ENEMIES = 'Creatures and Enemies'
    ITEMS = 'Items'
    LEGACY_DUNGEONS = 'Legacy Dungeons'
    LOCATIONS = 'Locations'
    NPCS = 'NPCs'
    SHIELDS = 'Shields'
    SKILLS = 'Skills'
    SPELLS = 'Spells'
    TALISMANS = 'Talismans'
    WEAPONS = 'Weapons'

category_paths = {
    EntityCategory.BOSSES: PATH_BOSSES,
    EntityCategory.ENEMIES: PATH_CREATURES_AND_ENEMIES,
    EntityCategory.ITEMS: PATH_ITEMS,
    EntityCategory.LEGACY_DUNGEONS: PATH_LEGACY_DUNGEONS,
    EntityCategory.LOCATIONS: PATH_LOCATIONS,
    EntityCategory.NPCS: PATH_NPCS,
    EntityCategory.SHIELDS: PATH_SHIELDS,
    EntityCategory.SKILLS: PATH_SKILLS,
    EntityCategory.SPELLS: PATH_SPELLS,
    EntityCategory.TALISMANS: PATH_TALISMANS, 
}

class Entity:
    def __init__(self, name, path='', category=None, image=None, content=''):
        self.name = name
        self.path = path
        self.category = category
        self.image = image
        self.content = content

    def __str__(self):
        name_f_string = f"\n{self.name}\n\
========\n\n"

        content_f_string = f"{self.content}"

        """
        name_f_string = f"\n{self.name}\n\
========\n\n"

        description_f_string = f"DESCRIPTION\n\
--------\n\
{self.description}\n\n"

        location_f_string = ''
        if self.location != '':
            location_f_string = f"LOCATION\n\
--------\n\
{self.location}\n\n"

        use_f_string = ''
        if self.use != '':
            use_f_string = f"USE\n\
--------\n\
{self.use}\n\n"

        notes_f_string = ''
        if self.notes != '':
            notes_f_string = f"NOTES & TIPS\n\
--------\n\
{self.notes}\n"
"""

        return name_f_string + content_f_string
    
    def __setattr__(self, name, value):
        if name == "content":
            markdown = md(value)
            markdown = Formatter.remove_nbsp(markdown)
            markdown = Formatter.remove_other_notes_bullet(markdown)
            markdown = Formatter.reformat_links(markdown)

            markdown = Formatter.remove_extra_spaces(markdown)

            markdown = Formatter.perform_targeted_corrections(self.name, markdown)
            self.__dict__[name] = markdown
        else:
            self.__dict__[name] = value

    def derive_path(self):
        self.path = '/' + self.name.replace(' ', '+')

    def format_links(self, md_text):
        md_text_whitespace_fixed = md_text.replace(u'\xa0', ' ').strip() # Remove leading and trailing whitespace, and non-breaking spaces (&nbsp;)

        # Removals
        rx_hemorrhage = re.sub(r"\[\([0-9]+\)\]\(\/Hemorrhage[^\)]+\)", "", md_text_whitespace_fixed)
        rx_remove_video_links = re.sub(r"\[Video[^\]]+\]\([^\)]+\)", "", rx_hemorrhage)

        # Reformatting
        rx_map_links = re.sub(r"[\[]+([^\]]+)\]\((\/[I|i]nteractive\+[M|m]ap\?[^\ ]+) \"([^\"]+)\"\)\]*\.*", r"[\1](\1)", rx_remove_video_links) # Fix map links
        # Now that all map links are in the same format, remove the generic ones i.e. not those that point toward a specific entity or location ("Elden Ring Map here", "Map Link", etc.)
        rx_remove_map_links = re.sub(r"\[(Elden Ring Map here|Map Coordinates|Map [Ll]ink|Elden Ring Map( [Ll]ink)*)\]\(\1\)", r"", rx_map_links)
        rx_links = re.sub(r"\[([^]]+)\]\(\/([^?\[\]]+) \"Elden Ring ([^\[\]]+)\"\)", r"[[\3|\1]]", rx_remove_map_links) # Reformat links
        
        # Due diligence
        rx_other_notes = re.sub(r"\* Other notes and player tips go here\.*", r"", rx_links)
        rx_unlink_builds = re.sub(r"\[\[Builds#[^\|]+\|([^\]]+)\]\]", r"\1", rx_other_notes)
        rx_special_weaknesses = re.sub(r"\[\[Special Weaknesses#[^\]]+\|([^\]]+)\]\]", r"\1", rx_unlink_builds)
        rx_ash_of_war_skill_links = re.sub(r"\[\[Ash of War: ", r"[[", rx_special_weaknesses)
        rx_condense_multispaces = re.sub(r" +", r" ", rx_ash_of_war_skill_links) # Condense multiple spaces

        corrections_applied = self.perform_targeted_corrections(rx_condense_multispaces)

        return corrections_applied

    def set_location(self, location_in_html):
        self.location = md(location_in_html.strip().replace(u'\xa0', ' '))

    def write(self, additional_tags=[], filename=None):

        if filename is None:
            filename = self.name

        path = LOCAL_CACHE + LOCAL_VAULT_NAME
        if self.category is not None:
            path += self.category.value + "/"
        # Create destination directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)
        
        f = open(path + filename+'.md', 'w')
        
        tags_md_string = ""
        # Front matter formatting--works, but ugly!
        # if additional_tags == []:
        #     additional_tags = ""
        # else:
        #     additional_tags = "\n- " + "\n- ".join(additional_tags)
        # tags_md_string = f"---\ntags:\n- {self.category.value}{additional_tags}\n---\n\n"
        if self.category is not None:
            category_string = re.sub(r" +", r"", self.category.value)
            tags_md_string = f"#{category_string}\n\n"

        image = ""
        if self.image is not None:
            image = "![["+self.image.name+"]]\n"

        content_md_string = ""
        if self.content != "":
            content_md_string = f"{self.content}\n\n"
        
        # description_md_string = ""
        # if self.description != "":
        #     description_md_string = f"## Description\n\n{self.description}\n\n"

        # location_md_string = ""
        # if self.location != "":
        #     location_md_string = f"## Location\n\n{self.location}\n\n"

        # use_md_string = ""
        # if self.use != "":
        #     use_md_string = f"## Use\n\n{self.use}\n\n"

        # notes_md_string = ""
        # if self.notes != "":
        #     notes_md_string = f"## Notes & Tips\n\n{self.notes}\n\n"

        #print(self.content)

        output_str = tags_md_string + image + content_md_string
        #print(output_str)
        f.write(output_str)
        f.close()

class Image:
    def __init__(self, data, name=''):
        self.data = data
        self.name = name
    
    def write(self, path=None):
        """
        Write image out to file.
        """
        destination_path = ''
        if path is not None:
            destination_path = path
        else:
            destination_path = LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS + self.name
        
        with open(destination_path, 'wb') as handler:
            handler.write(self.data)

class Dialogue:
    def __init__(self, context, line):
        self.context = context
        self.line = line

    def __str__(self):
        rep_str = "{}\n{}\n{}".format(self.name, self.type, self.description)
        #print(rep_str, self.name, self.type, self.description)
        return f'{self.name}\n{self.description}'
        
class NPC(Entity):
    def __init__(self, name, url='', category='', content=''):
        super().__init__(url, name, category=category, content=content)
