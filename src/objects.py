import os
import re
from enum import Enum

from markdownify import markdownify as md

from constants import *
from text_handling import Formatter

classes = [
    "Classes", 
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
    "Affinities", 
    "HP", 
    "FP", 
    "PvP", 
    "Poise", 
    "Robustness", 
    "Immunity", 
    "Equip Load", 
    "Physical Damage", 
    "Standard Damage", 
    "Strike Damage", 
    "Pierce Damage", 
    "Slash Damage", 
    "Critical Damage", 
    "Lightning Damage", 
    "Holy Damage", 
    "Fire Damage", 
    "Physical Defense", 
    "Standard Defense", 
    "Strike Defense", 
    "Pierce Defense", 
    "Slash Defense", 
    "Critical Defense", 
    "Lightning Defense", 
    "Holy Defense", 
    "Fire Defense", 
    "damage types", 
]

status_effects = [
    "Status Effects", 
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
    "Weapons", 
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
    "Bell Bearings", 
    "Smithing Stones", 
    "Somber Smithing Stones", 
    "Patch Notes", 
    "Creatures and Enemies", 
    "New Game Plus", 
    "Upgrades", 
    "Crafting", 
    "Crafting Materials", 
    "Cookbooks", 
    "Builds", 
    "Parry", 
    "Parrying", 
    "Sites of Grace", 
    "Site of Grace", 
    "Skeletons", 
    "Stance", 
    "NPC Summons", 
    "NPC Invaders", 
    "Spirit Ashes", 
    "Gestures", 
    "Bosses", 
    "Lore", 
    "NPCs", 
    "Great Runes", 
    "Smithing Stone", 
    "Stake of Marika", 
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

class Category(Enum):
    NONE = 'None'
    BOSSES = 'Bosses'
    ENEMIES = 'Creatures and Enemies'
    HIDDEN = 'Hidden'
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
    SPIRIT_ASH = 'Spirit Ashes'

category_paths = {
    Category.BOSSES: PATH_BOSSES,
    Category.ENEMIES: PATH_CREATURES_AND_ENEMIES,
    Category.ITEMS: PATH_ITEMS,
    Category.LEGACY_DUNGEONS: PATH_LEGACY_DUNGEONS,
    Category.LOCATIONS: PATH_LOCATIONS,
    Category.NPCS: PATH_NPCS,
    Category.SHIELDS: PATH_SHIELDS,
    Category.SKILLS: PATH_SKILLS,
    Category.SPELLS: PATH_SPELLS,
    Category.TALISMANS: PATH_TALISMANS, 
    Category.ARMOR: PATH_ARMOR, 
    Category.SPIRIT_ASH: PATH_SPIRIT_ASHES, 
}

name_overrides = {
    "Ranni the Witch":      "Ranni", 
    "Preceptor Seluvis":    "Seluvis", 
    "Monstrous Dog":        "Giant Dog", 
    "Monstrous Crow":       "Giant Crow", 
    "Cathedral of Dragon Communion (Caelid)":   "Cathedral of Dragon Communion"
}

class Entity:
    def __init__(self, name, category=Category.NONE, image=None):
        self.path = '/' + name.replace(' ', '+')    # Set the original path before we potentially remap name
        
        try:
            name = name_overrides[name]
        except KeyError:
            pass
        self.name = re.sub(r"\:", r",", name)  # Filenames can't have colons
        
        self.category = category
        self.image = image

        self.tags = []
        if category != Category.NONE:
            self.tags.append(re.sub(r" +", r"", category.value))

        # Hide "About" items
        if re.search(r"^About ", self.name):
            self.add_tag("Hidden")
        
        self.content = ""
        
    def __str__(self):
        name_f_string = f"\n{self.name}\n========\n\n"

        content_f_string = f"{self.content}"

        return name_f_string + content_f_string
    
    def __setattr__(self, name, value):
        if name == 'content':
            if value == "":
                self.__dict__[name] = value
                return
            # print(value)
            markdown = md(value)
            markdown = Formatter.remove_hemorrhage_links(markdown)
            markdown = Formatter.remove_video_links(markdown)
            markdown = Formatter.reformat_map_links(markdown)
            markdown = Formatter.remove_map_links(markdown)

            markdown = Formatter.replace_special_characters(markdown)
            markdown = Formatter.condense_newlines(markdown)
            markdown = Formatter.remove_other_notes_bullet(markdown)

            markdown = Formatter.reformat_links(markdown)
            markdown = Formatter.remove_anchor_links(markdown)

            markdown = Formatter.remove_extra_spaces(markdown)

            # Misc
            markdown = Formatter.unlink_builds(markdown)
            markdown = Formatter.unlink_special_weaknesses(markdown)
            markdown = Formatter.correct_crucible_aspect_spell_names(markdown)
            markdown = Formatter.redirect_ashofwar_skill_links(markdown)
            markdown = Formatter.replace_varre_e(markdown)

            # Unify inconsistent links/names
            markdown = Formatter.unify_champion_bracers(markdown)
            markdown = Formatter.unify_raging_wolf_gauntlets(markdown)
            markdown = Formatter.unify_alexander(markdown)
            markdown = Formatter.unify_boc(markdown)
            markdown = Formatter.unify_rat(markdown)
            markdown = Formatter.unify_celebrant(markdown)
            markdown = Formatter.unify_vulgar_militiamen(markdown)
            markdown = Formatter.unify_miranda_sprout(markdown)
            markdown = Formatter.unify_giant_miranda_sprout(markdown)
            markdown = Formatter.unify_lesser_mad_pumpkin_head(markdown)
            markdown = Formatter.unify_school_of_graven_mages(markdown)
            markdown = Formatter.unify_swamp_of_aeonia(markdown)
            
            markdown = Formatter.unify_d(markdown)
            markdown = Formatter.unify_eleonora(markdown)
            markdown = Formatter.unify_ranni(markdown)
            markdown = Formatter.unify_hewg(markdown)
            markdown = Formatter.unify_iji(markdown)
            markdown = Formatter.unify_godfrey(markdown)

            markdown = Formatter.unify_leyndell(markdown)
            markdown = Formatter.unify_ordina(markdown)
            markdown = Formatter.unify_gelmir(markdown)
            markdown = Formatter.unify_raya_lucaria(markdown)
            markdown = Formatter.unify_liurnia(markdown)

            # Convert custom text markers to Markdown
            markdown = Formatter.reformat_notes(markdown)
            markdown = Formatter.reify_bullets(markdown)

            if self.category not in [Category.ARMOR]:
                markdown = Formatter.remove_notes_after_sell_value(markdown)

            if self.category in [Category.NPCS]:
                markdown = Formatter.clean_dialogue(markdown)

            if self.category in [Category.ENEMIES]:
                pass

            # markdown = Formatter.remove_enemies_table(markdown)
            # markdown = Formatter.remove_npcs_table(markdown)
            # markdown = Formatter.remove_locations_table(markdown)
            # markdown = Formatter.remove_key_items_table(markdown)
            # markdown = Formatter.remove_bell_bearings_table(markdown)

            markdown = Formatter.remove_category_links_table(markdown)
            markdown = Formatter.fix_drop_links_inside_tables(markdown)
            markdown = Formatter.add_headers_to_tables(markdown)

            markdown = Formatter.final_whitespace_cleanup(markdown)

            # Targeted corrections
            markdown = Formatter.perform_targeted_corrections(self.name, markdown)
            markdown = Formatter.condense_newlines(markdown)
            markdown = Formatter.final_whitespace_cleanup(markdown)
            # # print(repr(markdown))
            # # print(markdown)
            self.__dict__[name] = markdown
        else:
            self.__dict__[name] = value

    def add_tag(self, tag):
        tag = re.sub(r" +", r"", tag)
        if tag not in self.tags:
            self.tags.append(tag)

    # def derive_path(self):
    #     self.path = '/' + self.name.replace(' ', '+')

    def set_location(self, location_in_html):
        self.location = md(location_in_html.strip().replace(u'\xa0', ' '))

    def write(self, additional_tags=[], filename=None):

        if filename is None:
            filename = re.sub(r"\:", r",", self.name)

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
        # if self.category is not None:
        #     category_string = re.sub(r" +", r"", self.category.value)
        #     self.tags.insert(0, category_string)
        #     # print(tags)
        tags = ["#"+tag for tag in self.tags]
        # print(tags)
        tags_md_string = " ".join(tags) + f"\n\n"

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
