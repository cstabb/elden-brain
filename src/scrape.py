import logging
import os
import re
import time
from enum import Enum

import requests
from bs4 import BeautifulSoup as bs
from markdownify import markdownify as md

# List of entities that exhibit parsing issues due to inconsistency with other similar pages
weapons_blacklist = ["Miquellan Knight's Sword", "Greataxe"]
items_blacklist = []
spells_blacklist = ["Placidusax's Ruin"]
bosses_blacklist = ["Dragonkin Soldier"]

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
url_t1_equipmentandmagic = "/Equipment+&+Magic"

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
url_t2_bosses = WIKI_BASE_URL + "/Bosses"

url_t2_locations = WIKI_BASE_URL + "/Locations"

url_t2_npcs = WIKI_BASE_URL + "/NPCs"

## Path final destination URLs
# (Most of these will be parsed from lists on mid-level pages)

url_t3_lore = WIKI_BASE_URL + "/Lore" # Used for scraping transcripts

## Stretch Goals
url_t3_effigies_of_the_martyr = WIKI_BASE_URL + "/Effigies+of+the+Martyr"
url_t3_sites_of_grace = WIKI_BASE_URL + "/Sites+of+Grace"
url_t3_sites_of_grace = WIKI_BASE_URL + "/Bell+Bearings"
### TORRENT REMINDER - PAGE NOT WORTH SCRAPING

## Tags
# (Most of these are derived)
HIDDEN_TAG = "#hide"

class EntityType(Enum):
    WEAPON = 'Weapons'
    SHIELD = 'Shields'
    ITEM = 'Items'
    NPC = 'NPCs'
    SPELL = 'Spells'
    SKILL = 'Skills'
    LOCATION = 'Locations'
    ENEMY = 'Creatures and Enemies'
    BOSS = 'Bosses'

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

        # would use match here if Pylance recognized my interpreter as being newer than Python 3.10...
        if self.type == EntityType.WEAPON:
            if self.name == "Alabaster Lord's Sword":
                correction = re.sub(r"Alabaster Lords' Pull", r"Alabaster Lord's Pull", text)
            elif self.name == "Parrying Dagger":
                correction = re.sub(r"PATCHES BELL BEARING", r"Patches' Bell Bearing", text)
            elif self.name == "Bloodstained Dagger":
                correction = re.sub(r"#gsc\.tab=0", r"", text)
            elif self.name == "Royal Greatsword":
                correction = re.sub(r"\/\/Strength", r"Strength", text)
            elif self.name == "Vulgar Militia Saw":
                correction = re.sub(r"\+ \[Example farming route\]\(\/file\/Elden\-Ring\/vulgar\_militia\_saw\.png \"Example farming route\"\)", r"", text)
            elif self.name == "Flowing Curved Sword":
                correction = re.sub(r" See it on the +\.", r"", text)
            elif self.name == "Nox Flowing Hammer":
                correction = re.sub(r"\[\[(Flowing Form) \(Nox Flowing Hammer\)", r"[[\1", text)
            # elif self.name == "Bolt of Gransax":
            #     correction = re.sub(r"\[\[(Leyndell Royal Capital) \(Legacy Dungeon\)#[^\]]+\]\]", r"[[\1|\1]]", text)
            elif self.name == "Torch":
                #[\'\,\"\/\(\)\+ \.\|\[\]#\*\w\&\n]*
                correction = re.sub(r" ### Elden Ring Torch Moveset[\'\,\"\/\(\)\+ \.\|\[\]#\*\w\&\n]*", r"", text)
                #correction = re.sub(r"\n\n", r"\n", correction)

        return correction

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
        rx_other_notes = re.sub(r"Other notes and player tips go here\.*", r"", rx_links)
        rx_unlink_builds = re.sub(r"\[\[Builds#[^\|]+\|([^\]]+)\]\]", r"\1", rx_other_notes)
        rx_special_weaknesses = re.sub(r"\[\[Special Weaknesses#[^\]]+\|([^\]]+)\]\]", r"\1", rx_unlink_builds)
        rx_ash_of_war_skill_links = re.sub(r"\[\[Ash of War: ", r"[[", rx_special_weaknesses)
        rx_condense_multispaces = re.sub(r" +", r" ", rx_ash_of_war_skill_links) # Condense multiple spaces

        corrections_applied = self.perform_targeted_corrections(rx_condense_multispaces)

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
            category_string = re.sub(r" +", r"", self.category.value)
            tags_md_string = f"#{category_string}\n\n"

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

    legacy_dungeons = [
        "/Leyndell+Royal+Capital+(Legacy+Dungeon)", 
        "/Stormveil+Castle", 
        "/Raya+Lucaria+Academy",  
        "/Volcano+Manor", 
        "/Miquella's+Haligtree",
        "/Elphael,+Brace+of+the+Haligtree", 
        "/Crumbling+Farum+Azula", 
    ]

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

    #TODO: Return a list of entities instead of writing to files immediately
    def convert_urls_to_entities(urls, category=None):
        """
        """
        this_category = None
        if category is not None and type(category) == EntityType:
            this_category = category

        blacklist = weapons_blacklist + items_blacklist + spells_blacklist + bosses_blacklist

        log.info(f"Parsing {len(urls)} entities...")
        for idx, endpoint in enumerate(urls):
            entity_name = endpoint.split('/')[-1].replace('+', ' ')
            if entity_name in blacklist:
                continue
            log.info(f"Parsing {entity_name} [{idx+1} of {len(urls)}]...")
            print(endpoint)
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
            #print(f"{entity_name}")
            entities.append(Entity(entity_name, category=EntityType.SKILL, description=description))
        
        return entities
    
    def url_to_entity(url, category=None, force_download_image=False):
        """
        """
        entity_name = Parser.convert_token_to_name(url.split("/")[-1])
        url = WIKI_BASE_URL + url

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

        description = ''
        for lineleft in content_block.find_all('div', attrs={'class', 'lineleft'}):
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
        drops_tokens = []
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
            elif 'Drops</h3>' in element_str.lower():
                mode = 'DROPS'
            elif 'tips</h3>' in element_str.lower():
                # print("MODE SET TO NOTES_AND_TIPS")
                mode = 'NOTES_AND_TIPS'
            elif 'use</h3>' in element_str.lower():
                mode = 'USE'
            elif 'click below for a list of all possible ashes of war that can be applied to' in element_str.lower():
                mode = 'ASHES_OF_WAR'
            #'<h3 class="bonfire">Elden Ring Torch Moveset'
            elif '<h3 class="bonfire">moveset' in element_str.lower():
                mode = 'MOVESET'

            #print(f"MODE = {mode}\n=================\n{element_str}\n^^^^^^^^^^^^^^^^\n")

            # Append to section list depending on current mode
            if mode == 'LOCATION':
                location_tokens.append(str(element))
            if mode == 'DROPS':
                drops_tokens.append(str(element))
            elif mode == 'NOTES_AND_TIPS':
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

    def get_weapons_urls():
        """
        """
        response = requests.get(url_t2_weapons)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            urls.append(destination)

        return urls

    def get_shields_urls():
        """
        """
        response = requests.get(url_t2_shields)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('h4'):
            for link in item.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
                print(link)
                destination = link.get('href')
                urls.append(destination)

        urls = list(set(urls)) # Unique

        return urls

    def get_spirit_ashes_urls():
        """
        """
        response = requests.get(url_t2_spirit_ashes)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            urls.append(destination)

        return urls

    def get_items_urls():
        """
        """
        response = requests.get(url_t2_items)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            urls.append(destination)
        
        urls = urls   # Last several elements contain throwaway urls
        
        urls = set(urls)    # Unique the values
        
        exclude = {
            "/Interactive+map?id=4605&lat=-93.653126&lng=115.069298&zoom=8&code=mapA",
        }

        urls = urls - exclude   # drop Legacy Dungeons from list

        return list(urls)
    
    def get_talisman_urls():
        """
        """
        response = requests.get(url_t2_talismans)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            urls.append(destination)

        return urls

    def get_spells_urls():
        """
        """
        response = requests.get(url_t2_spells)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for content in content_block.find_all('div', attrs={'class': 'tabcontent 0-tab tabcurrent'}):
            for item in content.find_all('h4', attrs={'style': 'text-align: center;'}):
                for link in item.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
                    destination = link.get('href')
                    urls.append(destination)

        urls = list(set(urls)) # Unique

        return urls

    def get_legacy_dungeons_urls():
        return Parser.legacy_dungeons

    def get_locations_urls():
        """
        """
        response = requests.get(url_t2_locations)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        urls = []
        for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'row'})):
            for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = link.get('href')
                urls.append(destination)

        urls = urls[0:-6]   # Last several elements contain throwaway urls
        
        urls = set(urls)    # Unique the values
        print(Parser.legacy_dungeons)
        exclude =  set(Parser.legacy_dungeons + ["/Legacy+Dungeons"])

        urls = urls - exclude   # drop Legacy Dungeons from list

        return list(urls)

    def get_locations_urls():
        """
        """
        response = requests.get(url_t2_locations)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        urls = []
        for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'row'})):
            for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = link.get('href')
                urls.append(destination)

        urls = urls[0:-6]   # Last several elements contain throwaway urls
        
        urls = set(urls)    # Unique the values
        print(Parser.legacy_dungeons)
        exclude =  set(Parser.legacy_dungeons + ["/Legacy+Dungeons"])

        urls = urls - exclude   # drop Legacy Dungeons from list

        return list(urls)
    
    def get_bosses_urls():
        """
        """
        response = requests.get(url_t2_bosses)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        urls = []
        for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'tabcontent 0-tab tabcurrent'})):
            for line in row.find_all('li'):
            # for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = line.a.get('href')
                urls.append(destination)

        return urls

    def get_armor_urls():
        """
        """
        response = requests.get(url_t2_armor)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        urls = []
        
        #TODO

        return urls

    def get_creatures_and_enemies_urls():
        """
        """
        response = requests.get(url_t2_creaturesandenemies)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        urls = []
        # for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'row'})):
        for idx, content in enumerate(content_block.find_all('div', attrs={'class': 'tabcontent 1-tab'})):
            for link in content.find_all('a', attrs={'class': 'wiki_link'}):
                #print(link)
                destination = link.get('href')
                print(destination)
                urls.append(destination)
        
        urls = set(urls)    # Unique the values
        
        exclude = {
            "/NPC+Invaders", 
        }

        urls = urls - exclude   # drop Legacy Dungeons from list
        
        return list(urls)

    def get_npcs_urls():
        """
        """
        response = requests.get(url_t2_npcs)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        urls = []
        for idx, row in enumerate(content_block.find_all('div', attrs={'id': 'reveal'})):
            for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = link.get('href')
                destination = '/' + destination.split('/')[-1]
                urls.append(destination)

        urls = set(urls)    # Unique the values
        
        exclude = {
            "/Isolated+Merchants", 
            "/Nomadic+Merchants", 
            "/Volcano+Manor+Spirit", 
        }

        urls = urls - exclude   # drop Legacy Dungeons from list

        return list(urls)

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
            "Standard Damage", 
            "Strike Damage", 
            "Critical Damage", 
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

        self.spell_type = [
            "Sorceries", 
            "Incantations", 
            "Bestial Incantations", 
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

        self.shield_type = [
            "Small Shields", 
            "Medium Shields", 
            "Greatshields", 
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
            "Patch Notes", 
            "Creatures and Enemies", 
            "New Game Plus", 
            "Upgrades", 
            "Crafting Materials", 
            "Cookbooks", 
        ]
        # Create directories if they don't already exist
        if not os.path.exists(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY):
            os.mkdir(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY)
        if not os.path.exists(CACHE_LOCATION + VAULT_NAME + HIDDEN_WRITE_DIRECTORY):
            os.mkdir(CACHE_LOCATION + VAULT_NAME + HIDDEN_WRITE_DIRECTORY)

    def create_skills(self, overwrite=True):
        """
        """
        skill_entities = Parser.get_skill_entities()

        log.info(f"Parsing {len(skill_entities)} Skills...")
        
        for idx, skill in enumerate(skill_entities):
            log.info(f"Creating {skill.name} [{idx+1} of {len(skill_entities)}]...")
            skill.write_to_file()
            time.sleep(0.001)   # Necessary to allow Obsidian time to update with the new file
        
    def create_hidden(self, overwrite=True):
        all_targets = self.classes + self.stats + self.status_effects + \
                      self.weapon_type + self.shield_type + self.hide_list
        print(all_targets)
        destination_path = CACHE_LOCATION + VAULT_NAME + HIDDEN_WRITE_DIRECTORY

        log.info(f"Creating {len(all_targets)} hidden files...")

        for idx, target in enumerate(all_targets):
            # Create a new file if it doesn't exist or overwrite is True
            if overwrite or ~os.path.isfile(destination_path + target):
                log.info(f"Creating {target} hidden file [{idx+1} of {len(all_targets)}]...")
                f = open(destination_path + target + '.md', 'w')
                f.write(HIDDEN_TAG)
                f.close()
                time.sleep(0.001)   # Necessary to allow Obsidian time to update with the new file

    def create_weapons(self, overwrite=True):
        """
        """
        urls = Parser.get_weapons_urls()
        entities = Parser.convert_urls_to_entities(urls, EntityType.WEAPON)

        log.info(f"Parsing {len(entities)} {EntityType.WEAPON}...")
        
        for idx, entity in enumerate(entities):
            log.info(f"Creating {entity.name} [{idx+1} of {len(entities)}]...")
            entity.write_to_file()
            #time.sleep(0.001)

    def create_shields(self, overwrite=True):
        """
        """
        urls = Parser.get_shields_urls()
        Parser.convert_urls_to_entities(urls, EntityType.SHIELD)

    def create_armor(self, overwrite=True):
        #TODO
        pass

    def create_items(self, overwrite=True):
        """
        """
        urls = Parser.get_items_urls()
        entities = Parser.convert_urls_to_entities(urls, EntityType.ITEM)

    def create_locations(self, overwrite=True):
        """
        """
        urls = Parser.get_locations_urls()
        Parser.convert_urls_to_entities(urls, EntityType.LOCATION)

    def create_legacy_dungeons(self, overwrite=True):
        """
        """
        urls = Parser.get_legacy_dungeons_urls()
        print(urls)
        print(len(urls))
        Parser.convert_urls_to_entities(urls, EntityType.LOCATION)

    def create_spells(self, overwrite=True):
        """
        """
        urls = Parser.get_spells_urls()
        Parser.convert_urls_to_entities(urls, EntityType.SPELL)

    def create_spirit_ashes(self, overwrite=True):
        #TODO
        pass

    def create_creatures_and_enemies(self, overwrite=True):
        """
        """
        urls = Parser.get_creatures_and_enemies_urls()
        Parser.convert_urls_to_entities(urls, EntityType.ENEMY)

    def create_bosses(self, overwrite=True):
        """
        """
        urls = Parser.get_bosses_urls()
        # print(urls)
        # print(len(urls))
        Parser.convert_urls_to_entities(urls, EntityType.BOSS)

    def create_npcs(self, overwrite=True):
        """
        """
        urls = Parser.get_npcs_urls()
        Parser.convert_urls_to_entities(urls, EntityType.NPC)

def main():

    eb = EldenBring()

    # eb.create_skills() # WORKS
    # eb.create_hidden() # WORKS
    # eb.create_weapons() # WORKS
    # eb.create_shields() # WORKS
    # eb.create_armor()
    # eb.create_locations() # WORKS
    # eb.create_legacy_dungeons() # NEEDS SPECIAL PAGE PARSING
    # eb.create_spells() # WORKS
    # eb.create_spirit_ashes()
    # eb.create_creatures_and_enemies() # WORKS
    eb.create_bosses()
    # eb.create_npcs() # WORKS

    # Create destination directory if it doesn't exist
    # if not os.path.exists(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY):
    #     os.mkdir(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY)

    # all_endpoints = get_all_endpoints()

    # all_item_urls = Parser.get_items_urls()
    # print(all_item_urls)
    # print(len(all_item_urls))
    # f = open(CACHE_LOCATION + VAULT_NAME + 'temp.txt', 'w')
    # f.write('\n'.join(list(set(all_item_urls))))
    # f.close()
    # Parser.convert_urls_to_entities(all_item_urls, EntityType.ITEM)

    # all_legacy_dungeon_urls = Parser.get_legacy_dungeon_urls()
    # print(all_legacy_dungeon_urls)

    # all_weapon_urls = Parser.get_weapons_urls()
    # Parser.convert_urls_to_entities(all_weapon_urls, EntityType.WEAPON)

    # all_location_urls = Parser.get_location_urls()
    # print(len(all_location_urls))
    # Parser.convert_urls_to_entities(all_location_urls, EntityType.LOCATION)

    # f = open(CACHE_LOCATION + VAULT_NAME + 'temp.txt', 'w')
    # f.write('\n'.join(list(set(all_location_urls))))
    # f.close()
    # print(all_location_urls)

    ## NPCS
    # all_npcs_urls = Parser.get_npcs_urls()
    # print(all_npcs_urls)
    # print(len(all_npcs_urls))
    # Parser.convert_urls_to_entities(all_npcs_urls, EntityType.NPC)
    
    
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

    # Torch
    # torch = Parser.url_to_entity(WIKI_BASE_URL+"/Torch", EntityType.WEAPON, force_download_image=False)
    # print(torch)
    # torch.write_to_file()

if __name__=="__main__":
    main()