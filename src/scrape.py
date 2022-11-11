import logging
import os
import re
from enum import Enum

import requests
from bs4 import BeautifulSoup as bs
from markdownify import markdownify as md

# List of entities that exhibit parsing issues due to inconsistency with other similar pages
blacklist = ["Miquellan Knight's Sword", "Greataxe"]

# Set up logger
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("elden-bring-logger")

WIKI_BASE_URL = "https://eldenring.wiki.fextralife.com"

## File Locations
CACHE_LOCATION = "cache/"
VAULT_NAME = "Elden Ring/"
IMAGE_WRITE_DIRECTORY = "Assets/" # If this is set, also set Obsidian's Attachment folder path to the same value (found in Settings->Files & Links)
HIDDEN_WRITE_DIRECTORY = "Hidden/"

### URLs

## Top-level URLs
url_t1_equipmentandmagic = "https://eldenring.wiki.fextralife.com/Equipment+&+Magic"

## Mid-Level URLs

url_t2_weapons = WIKI_BASE_URL + "/Weapons"
url_t2_spirit_ashes = WIKI_BASE_URL + "/Spirit+Ashes"
url_t2_skills = WIKI_BASE_URL + "/Skills"
url_t2_spells = WIKI_BASE_URL + "/Magic+Spells"
url_t2_shields = WIKI_BASE_URL + "/Shields"
url_t2_armor = WIKI_BASE_URL + "/Armor"
url_t2_talismans = WIKI_BASE_URL + "/Talismans"
url_t2_items = WIKI_BASE_URL + "/Items"

url_t2_creaturesandenemies = WIKI_BASE_URL + "/Creatures+and+Enemies"

url_t2_locations = WIKI_BASE_URL + "/Locations"

url_t2_npcs = WIKI_BASE_URL + "/NPCs"

## Path final destination URLs
# (Most of these will be parsed from lists on mid-level pages)

url_t3_lore = WIKI_BASE_URL + "/Lore" # Used for scraping transcripts

## Tags
# (Most of these are derived)
HIDDEN_TAG = "#hide"

class EntityType(Enum):
    WEAPON = 'Weapons'
    ITEM = 'Items'
    NPC = 'NPCs'
    SPELL = 'Spells'
    SKILL = 'Skills'

class Entity:
    def __init__(self, name, url='', category=None, image=None, type='', header='', description='', location='', use='', notes=''):
        self.name = name
        self.url = url
        self.category = category
        self.image = image
        #TODO: assert type is EntityType before assignment
        self.type = type
        self.header = self.format_links(md(header, strip=["img"])) # Initial description paragraph
        self.description = self.format_links(md(description, strip=["img"]))
        self.location = self.format_links(md(location, strip=["img"]))
        self.use = self.format_links(md(use, strip=["img"]))
        self.notes = self.format_links(md(notes, strip=["img"]))

    def __str__(self):
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

        return name_f_string + description_f_string + location_f_string + use_f_string + notes_f_string

    def perform_targeted_corrections(self, text=""):
        correction = text
        if self.name == "Alabaster Lord's Sword":
            correction = re.sub(r"Alabaster Lords' Pull", r"Alabaster Lord's Pull", text)
        elif self.name == "Parrying Dagger":
            correction = re.sub(r"PATCHES BELL BEARING", r"Patches' Bell Bearing", text)
        elif self.name == "Bloodstained Dagger":
            correction = re.sub(r"#gsc\.tab=0", r"", text)

        return correction

    def format_links(self, md_text):
        md_text_whitespace_fixed = md_text.replace(u'\xa0', ' ').strip() # Remove leading and trailing whitespace, and non-breaking spaces (&nbsp;)

        # Due diligence
        rx_condense_multispaces = re.sub(r" +", r" ", md_text_whitespace_fixed) # Condense multiple spaces

        # Removals
        rx_hemorrhage = re.sub(r"\[\([0-9]+\)\]\(\/Hemorrhage[^\)]+\)", "", rx_condense_multispaces)
        map_link_insertion = r"[\1](" + WIKI_BASE_URL + r"/\2)" # Use this string in the below regex to keep external map links
        # rx_remove_map_links = re.sub(r"\[\[(Elden Ring [M|m]ap[^\)]+|[M|m]ap [lL]ink|Map Coordinates)\]\((\/[I|i]nteractive\+[M|m]ap\?[^\ ]+)( \"[^\[]+\"\)\])", "", rx_hemorrhage) # Fix map links
        rx_remove_map_links = re.sub(r"\[+([^M|m]*[M|m]ap[^\]]+)\]\((\/[I|i]nteractive\+[M|m]ap\?[^\ ]+)( \"[^\[]+\"\)\]*)", "", rx_hemorrhage) # Fix map links
        rx_remove_video_links = re.sub(r"\[Video[^\]]+\]\([^\)]+\)", "", rx_remove_map_links)

        # Reformatting
        rx_links = re.sub(r"\[([^]]+)\]\(\/([^?\[\]]+) \"Elden Ring ([^\[\]]+)\"\)", r"[[\3|\1]]", rx_remove_video_links) # Reformat links
        
        #rx4 = re.sub(r"\(\/Interactive\+Map[^\)]+\)", "", rx3) # Scrub all map links

        corrections_applied = self.perform_targeted_corrections(rx_links)

        return corrections_applied

    def set_location(self, location_in_html):
        self.location = md(location_in_html.strip().replace(u'\xa0', ' '))

    def write_to_file(self, additional_tags=[], filename=None):

        if filename is None:
            filename = self.name

        path = CACHE_LOCATION + VAULT_NAME
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
            tags_md_string = f"#{self.category.value}\n\n"

        image = ""
        if self.image is not None:
            image = "![["+self.image.url.split("/")[-1]+"]]\n"
        
        description_md_string = ""
        if self.description != "":
            description_md_string = f"## Description\n\n{self.description}\n\n"

        location_md_string = ""
        if self.location != "":
            location_md_string = f"## Location\n\n{self.location}\n\n"

        use_md_string = ""
        if self.use != "":
            use_md_string = f"## Use\n\n{self.use}\n\n"

        notes_md_string = ""
        if self.notes != "":
            notes_md_string = f"## Notes & Tips\n\n{self.notes}\n\n"

        output_str = tags_md_string + image + description_md_string + location_md_string + use_md_string + notes_md_string
        
        f.write(output_str)
        f.close()

class Image:
    def __init__(self, url, name=''):
        self.url = url
        self.name = (name if name != '' else self.derive_name_from_url())

    def derive_name_from_url(self):
        return Parser.convert_token_to_name(Parser.get_url_last_token(self.url))
    
    def write_to_file(self, filename=None):
        image_extension = self.url.split('.')[-1]
        image_data = requests.get(self.url).content
        destination_path = ''
        if filename is not None:
            destination_path = filename
        else:
            destination_path = CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY + self.name
        with open(destination_path, 'wb') as handler:
            handler.write(image_data)

class Dialogue:
    def __init__(self, context, line):
        self.context = context
        self.line = line

    def __str__(self):
        rep_str = "{}\n{}\n{}".format(self.name, self.type, self.description)
        #print(rep_str, self.name, self.type, self.description)
        return f'{self.name}\n{self.description}'
        
class NPC(Entity):
    def __init__(self, name, url='', type='', header='', notes='', location='', dialogue=''):
        super().__init__(url, name, type, header, notes)
        self.location = location
        self.dialogue = dialogue

class Formatter:
    """
    """
    def write_entity_to_cli(entity):
        #assert(isinstance(entity, Entity), "not an entity")
    
        # TODO: Move formatting from entity to here
        print(entity)

class Writer:
    """
    """

class Parser:
    """
    Collection of functions to parse HTML pages into entities.
    """

    def get_url_last_token(url):
        """
        Get URL's last token
        """
        endpoint = url.split('/')[-1]
        return endpoint

    def convert_token_to_name(token):
        """
        Convert the last URL token to an entity name

        Tokens substitute a + for space, so this function substitutes a space for +
        """
        return token.replace('+', ' ')

    def convert_urls_to_entities(urls, category=None):
        """
        """
        this_category = None
        if category is not None and type(category) == EntityType:
            this_category = category

        log.info(f"Parsing {len(urls)} entities...")
        for idx, endpoint in enumerate(urls):
            entity_name = endpoint.split('/')[-1].replace('+', ' ')
            if entity_name in blacklist:
                continue
            log.info(f"Parsing {entity_name} [{idx+1} of {len(urls)}]...")
            entity = Parser.url_to_entity(endpoint, this_category, force_download_image=False)
            entity.write_to_file()

    def get_skill_entities():
        """
        Build a list of entities from the table on the Skills page

        This table contains descriptions, so visiting individual Skill pages is not necessary
        """
        url = url_t2_skills
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        entities = []
        rows = table_body.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            cells = [ele.text.strip() for ele in cells]
            
            entity_name = cells[0]
            description = cells[5]
            entities.append(Entity(entity_name, category=EntityType.SKILL, description=description))

        return entities
    
    def url_to_entity(url, category=None, force_download_image=False):
        """
        """
        entity_name = Parser.convert_token_to_name(url.split("/")[-1])

        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        #nonBreakSpace = u'\xa0'
        #soup = soup.replace('&nbsp;', ' ')
        #soup = bs(soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ')), 'html.parser')
        #print("SOUP = ", soup)

        # texts = soup.find_all(text=True)
        # for t in texts:
        #     newtext = t.replace("&nbsp", "")
        #     t.replace_with(newtext)
        # soup = bs(texts.text, 'html.parser')

        content_block = soup.find('div', attrs={"id": "wiki-content-block"})

        # Infobox
        infobox = content_block.find('div', attrs={'class', 'infobox'})

        # Process the item's main image
        image_tag = infobox.find('img') # First image is the one we want
        image_attr_src = image_tag['src']
        image_name = image_attr_src.split('/')[-1] # Get the target token
        image_url = WIKI_BASE_URL + image_attr_src
        image = Image(image_url)
        if force_download_image:
            image.write_to_file()
        else:
            # Download if file does not already exist
            if ~os.path.isfile(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY + image_name):
                image.write_to_file()

        all_img_tags = content_block.img
        all_img_tags.decompose()

        all_linelefts = content_block.find_all('div', attrs={'class', 'lineleft'})

        description = ''
        for lineleft in all_linelefts:
            # Get description
            paragraphs = lineleft.find_all('em')
            if len(paragraphs) == 0:
                continue
            #print(paragraphs)
            description_tokens = []
            for paragraph in paragraphs:
                #print("before: {}", paragraph)
                paragraph_text = paragraph.get_text(separator="\n").strip()
                #print("after: {}", paragraph_text)
                description_tokens.append(paragraph_text)
            description = "\n\n".join(description_tokens)

        mode = ''
        location_tokens = []
        notes_tokens = []
        use_tokens = []
        moveset_tokens = []
        ashes_of_war_tokens = []
        # Walk the block for the information
        # Recursive=False is necessary to avoid repeat nested tags
        for element in content_block.find_all(["h3", "p","ul"], recursive=False):
            #print("ELEMENT = ", str(element))
            element_str = str(element)
            #print("ELEMENT\n------------" + element_str)
            # Set Mode
            # This works by dint of the first element always being this string (guaranteed?)
            if '<h3 class="bonfire">where to find' in element_str.lower():
                mode = 'LOCATION'
            elif 'tips</h3>' in element_str.lower():
                # print("MODE SET TO NOTES_AND_TIPS")
                mode = 'NOTES_AND_TIPS'
            elif 'use</h3>' in element_str.lower():
                mode = 'USE'
            elif 'click below for a list of all possible ashes of war that can be applied to' in element_str.lower():
                mode = 'ASHES_OF_WAR'
            elif '<h3 class="bonfire">moveset' in element_str.lower():
                mode = 'MOVESET'

            #print(f"MODE = {mode}\n=================\n{element_str}\n^^^^^^^^^^^^^^^^\n")

            # Append to section list depending on current mode
            if mode == 'LOCATION':
                location_tokens.append(str(element))
            elif mode == 'NOTES_AND_TIPS':
                #print(mode)
                #print(str(element))
                notes_tokens.append(str(element))
            elif mode == 'USE':
                use_tokens.append(str(element))
            elif mode == 'ASHES_OF_WAR':
                #print(mode)
                ashes_of_war_tokens.append(str(element))
            elif mode == 'MOVESET':
                moveset_tokens.append(str(element))
        
        # Vagaries of the Notes & Tips section--
        # - Remove paragraphs
        # - Drop last two elements
        #notes_tokens = notes_tokens[1:-1]
        # if entity_type == EntityType.WEAPON:
        #     notes_tokens = list(filter(lambda c: c[0:2] != '<p', notes_tokens))[1:-2]
        
        # Vagaries of the Use section--
        # - Drop last element
        use_tokens = use_tokens[1:-1]

        # Vagaries of the Location section--
        # - Drop last element
        location_tokens = location_tokens[1:-1]

        #print(location_tokens)
        #print('\n'.join(map(str,location_tokens)))
        #print('\n\n')  
        #print(notes_tokens)
        #print(ashes_of_war_tokens)
        #print('\n'.join(map(str,notes_tokens)))

        #print(md(''.join(location_tokens)))

        #s.replace(u'\xa0', ' ')
        # Create Entity parts
        location = ' '.join(location_tokens)#.encode("ascii", "ignore")
        notes = ' '.join(notes_tokens)#.encode("ascii", "ignore")
        use = ' '.join(use_tokens)
        #print(entity_name)

        return Entity(entity_name, url, category=category, image=image, description=description, location=location, use=use, notes=notes)

    def get_weapons_urls(limit=None):
        """
        """
        response = requests.get(url_t2_weapons)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all Weapon objects from the main Weapons page
        weapon_urls = []
        i = 0
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            i += 1
            if i == 1:
                continue
            if limit is not None:
                if i > limit+1:
                    break

            destination = item.get('href')

            weapon_url = WIKI_BASE_URL + destination
            weapon_urls.append(weapon_url)

        return weapon_urls

    def get_items_urls(limit=None):
        """
        """
        response = requests.get(url_t2_items)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all Weapon objects from the main Weapons page
        item_urls = []
        i = 0
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            i += 1
            if i == 1:
                continue
            if limit is not None:
                if i > limit+1:
                    break

            destination = item.get('href')

            item_url = WIKI_BASE_URL + destination
            item_urls.append(item_url)

        return item_urls

# ====================================================

class EldenBring:
    """
    """

    def __init__(self):
        self.classes = [
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

        self.stats = [
            "Vigor", 
            "Mind", 
            "Endurance", 
            "Strength", 
            "Dexterity", 
            "Intelligence", 
            "Faith", 
            "Arcane", 
            "Discovery", 
        ]

        self.status_effects = [
            "Poison", 
            "Scarlet Rot", 
            "Blood Loss", 
            "Frostbite", 
            "Sleep", 
            "Madness", 
            "Death Blight", 
            "Hemorrhage", 
            "/Hemorrhage", # Erroneously created
        ]

        self.weapon_type = [
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

        self.hide_list = [
            "Ashes of War", 
            "Consumables", 
            "Magic", 
            "Magic Spells", 
            "Runes", 
            "Skills", 
            "Smithing Stones", 
            "Somber Smithing Stones", 
            "Incantations", 
            "Faith"
        ]
        # Create directories if they don't already exist
        if not os.path.exists(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY):
            os.mkdir(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY)
        if not os.path.exists(CACHE_LOCATION + VAULT_NAME + HIDDEN_WRITE_DIRECTORY):
            os.mkdir(CACHE_LOCATION + VAULT_NAME + HIDDEN_WRITE_DIRECTORY)

    def create_skills(self):
        """
        """
        skill_entities = Parser.get_skill_entities()

        log.info(f"Parsing {len(skill_entities)} Skills...")

        for skill in skill_entities:
            skill.write_to_file()
        
    def create_hidden(self, overwrite=True):
        all_targets = self.classes + self.stats + self.status_effects + self.weapon_type + self.hide_list
        print(all_targets)
        destination_path = CACHE_LOCATION + VAULT_NAME + HIDDEN_WRITE_DIRECTORY

        for idx, target in enumerate(all_targets):
            # Create a new file if it doesn't exist or overwrite is True
            if overwrite or ~os.path.isfile(destination_path + target):
                log.info(f"Creating {target} hidden file [{idx+1} of {len(all_targets)}]...")
                f = open(destination_path + target+'.md', 'w')
                f.write(HIDDEN_TAG)
                f.close()

def main():

    eb = EldenBring()

    eb.create_skills()
    eb.create_hidden()

    # Create destination directory if it doesn't exist
    # if not os.path.exists(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY):
    #     os.mkdir(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY)

    # all_endpoints = get_all_endpoints()
    # all_item_urls = Parser.get_items_urls()
    all_weapon_urls = Parser.get_weapons_urls()

    Parser.convert_urls_to_entities(all_weapon_urls, EntityType.WEAPON)
    
    # dagger = Parser.url_to_entity(WIKI_BASE_URL+"/Dagger", EntityType.WEAPON, force_download_image=False)
    # print(dagger)
    # dagger.write_to_file()

    # item = parse_endpoint_to_entity(WIKI_BASE_URL+"/Fingerslayer+Blade", force_download_image=False)
    # item = parse_endpoint_to_entity(WIKI_BASE_URL+"/Miquellan+Knight's+Sword", force_download_image=False)
    
    # giant_crusher = parse_endpoint_to_entity(WIKI_BASE_URL+"/Giant-Crusher", EntityType.WEAPON, force_download_image=False)
    # print(giant_crusher)
    # giant_crusher.write_to_file()

    # Cleanrot Knight's Sword
    # cleanrot_knights_sword = Parser.url_to_entity(WIKI_BASE_URL+"/Cleanrot+Knight's+Sword", EntityType.WEAPON, force_download_image=False)
    # print(cleanrot_knights_sword)
    # cleanrot_knights_sword.write_to_file()

    # ALABASTER LORD'S SWORD
    # alabaster_lords_sword = Parser.url_to_entity(WIKI_BASE_URL+"/Alabaster+Lord's+Sword", EntityType.WEAPON, force_download_image=False)
    # print(alabaster_lords_sword)
    # alabaster_lords_sword.write_to_file()

    # Parrying Dagger
    # parrying_dagger = Parser.url_to_entity(WIKI_BASE_URL+"/Parrying+Dagger", EntityType.WEAPON, force_download_image=False)
    # print(parrying_dagger)
    # parrying_dagger.write_to_file()

if __name__=="__main__":
    main()