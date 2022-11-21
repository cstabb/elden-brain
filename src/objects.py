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
    "Immunity", 
    "Standard Damage", 
    "Strike Damage", 
    "Pierce Damage", 
    "Slash Damage", 
    "Critical Damage", 
    "Lightning Damage", 
    "Holy Damage", 
    "Fire Damage", 
    "damage types", 
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
    "Instant Death", 
    "Hemorrhage", 
    "/Hemorrhage", 
]

items_to_hide = [
    "Ghost Glovewort (1)", 
    "Ghost Glovewort (2)", 
    "Ghost Glovewort (3)", 
    "Ghost Glovewort (4)", 
    "Ghost Glovewort (5)", 
    "Ghost Glovewort (6)", 
    "Ghost Glovewort (7)", 
    "Ghost Glovewort (8)", 
    "Ghost Glovewort (9)", 
    "Grave Glovewort (1)", 
    "Grave Glovewort (2)", 
    "Grave Glovewort (3)", 
    "Grave Glovewort (4)", 
    "Grave Glovewort (5)", 
    "Grave Glovewort (6)", 
    "Grave Glovewort (7)", 
    "Grave Glovewort (8)", 
    "Grave Glovewort (9)", 
    "Smithing Stone (1)", 
    "Smithing Stone (2)", 
    "Smithing Stone (3)", 
    "Smithing Stone (4)", 
    "Smithing Stone (5)", 
    "Smithing Stone (6)", 
    "Smithing Stone (7)", 
    "Smithing Stone (8)", 
    "Somber Smithing Stone (1)", 
    "Somber Smithing Stone (2)", 
    "Somber Smithing Stone (3)", 
    "Somber Smithing Stone (4)", 
    "Somber Smithing Stone (5)", 
    "Somber Smithing Stone (6)", 
    "Somber Smithing Stone (7)", 
    "Somber Smithing Stone (8)", 
    "Somber Smithing Stone (9)", 
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
    "Godslayer Incantations", 
    "Golden Order Incantations", 
    "Servants of Rot Incantations", 
    "Two Fingers Incantations", 
    "Two Fingers' Incantations", 
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

armor_type = [
    "Gauntlets", 
    "Helms", 
    "Chest Armor", 
    "Leg Armor", 
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
    "Site of Grace", 
    "Skeletons", 
    "Stance", 
    "NPC Summons", 
    "Spirit Ashes", 
    "Gestures", 
]

# List of entities that exhibit parsing issues due to inconsistency with other similar pages
weapons_blacklist = ["Upgrades"]    # "Miquellan Knight's Sword", "Greataxe"
items_blacklist = []
spells_blacklist = []   # "Placidusax's Ruin"
bosses_blacklist = []

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
    ARMOR = 'Armor'

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
    EntityCategory.ARMOR: PATH_ARMOR, 
}

class Entity:
    def __init__(self, name, path='', category=None, image=None, content=''):
        self.name = name
        self.path = path
        self.category = category
        self.image = image
        self.content = content

    def __str__(self):
        name_f_string = f"\n{self.name}\n========\n\n"

        content_f_string = f"{self.content}"

        return name_f_string + content_f_string
    
    def __setattr__(self, name, value):
        if name == "content":
            markdown = md(value)
            markdown = Formatter.remove_hemorrhage_links(markdown)
            markdown = Formatter.remove_video_links(markdown)
            markdown = Formatter.reformat_map_links(markdown)
            markdown = Formatter.remove_map_links(markdown)

            markdown = Formatter.replace_special_characters(markdown)
            markdown = Formatter.condense_newlines(markdown)
            markdown = Formatter.remove_other_notes_bullet(markdown)

            markdown = Formatter.reformat_links(markdown)

            markdown = Formatter.remove_extra_spaces(markdown)

            # Misc
            markdown = Formatter.unlink_builds(markdown)
            markdown = Formatter.unlink_special_weaknesses(markdown)
            markdown = Formatter.redirect_ashofwar_skill_links(markdown)
            markdown = Formatter.replace_varre_e(markdown)
            markdown = Formatter.unify_boc(markdown)
            markdown = Formatter.unify_rat(markdown)
            markdown = Formatter.unify_vulgar_militiamen(markdown)
            markdown = Formatter.unify_miranda_sprout(markdown)
            markdown = Formatter.unify_giant_miranda_sprout(markdown)
            markdown = Formatter.reify_bullets(markdown)

            if self.category not in [EntityCategory.ARMOR]:
                markdown = Formatter.remove_notes_after_sell_value(markdown)

            if self.category in [EntityCategory.NPCS]:
                markdown = Formatter.clean_dialogue(markdown)

            if self.category in [EntityCategory.ENEMIES]:
                pass

            if self.category in [EntityCategory.NPCS]:
                pass

            markdown = Formatter.remove_enemies_table(markdown)
            markdown = Formatter.remove_npcs_table(markdown)
            markdown = Formatter.remove_locations_table(markdown)

            markdown = Formatter.final_whitespace_cleanup(markdown)

            # Targeted corrections
            markdown = Formatter.perform_targeted_corrections(self.name, markdown)
            # print(repr(markdown))
            # print(markdown)
            self.__dict__[name] = markdown
        else:
            self.__dict__[name] = value

    def derive_path(self):
        self.path = '/' + self.name.replace(' ', '+')

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
            image = "![["+self.image.name+"]]\n\n"

        content_md_string = ""
        if self.content != "":
            content_md_string = f"{self.content}"

        output_str = tags_md_string + image + content_md_string
        
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
