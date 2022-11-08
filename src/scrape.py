import os
import re
import logging
from enum import Enum

import requests
from bs4 import BeautifulSoup as bs
from markdownify import markdownify as md

CACHE_LOCATION = "cache/"
VAULT_NAME = "Elden Ring/"
IMAGE_WRITE_DIRECTORY = "Assets/" # If this is set, also set Obsidian's Attachment folder path to the same value (found in Settings->Files & Links)
WIKI_BASE_URL = "https://eldenring.wiki.fextralife.com"

### URLs
## Top-level URLs

url_t1_equipmentandmagic = "https://eldenring.wiki.fextralife.com/Equipment+&+Magic"

## Mid-Level URLs
url_t2_creaturesandenemies = "https://eldenring.wiki.fextralife.com/Creatures+and+Enemies"
url_t2_items = "https://eldenring.wiki.fextralife.com/Items"
url_t2_weapons = "https://eldenring.wiki.fextralife.com/Weapons"

## Path final destination URLs
# (Most of these will be parsed from lists on mid-level pages)

class EntityType(Enum):
    WEAPON = 1
    SPELL = 2

class Entity:
    def __init__(self, name, url='', image=None, type='', header='', description='', location='', use='', notes=''):
        self.name = name
        self.url = url
        self.image = image
        #TODO: assert type is EntityType before assignment
        self.type = type
        self.header = self.format_links(md(header, strip=["img"])) # fextralife's initial description paragraph
        self.description = self.format_links(md(description, strip=["img"]))
        self.location = self.format_links(md(location, strip=["img"]))
        self.use = self.format_links(md(use, strip=["img"]))
        self.notes = self.format_links(md(notes, strip=["img"]))

    def __str__(self):
        return f"\n\
{self.name}\n\
========\n\n\
DESCRIPTION\n\
--------\n\
{self.description}\n\n\
LOCATION\n\
--------\n\
{self.location}\n\n\
USE\n\
--------\n\
{self.use}\n\n\
NOTES & TIPS\n\
--------\n\
{self.notes}\n"

    def format_links(self, md_text):
        md_text_whitespace_fixed = md_text.replace(u'\xa0', ' ').strip() # Remove leading and trailing whitespace, and non-breaking spaces (&nbsp;)
        rx1 = re.sub(r" +", r" ", md_text_whitespace_fixed) # Condense multiple spaces
        rx2 = re.sub(r"\[([^()]+)\]\(\/([^?\[\]]+) \"Elden Ring ([^\[\]]+)\"\)", r"[[\3|\1]]", rx1) # Reformat links
        rx3 = re.sub(r"\[(Elden Ring Map Link)\]\((\/Interactive\+Map\?[^\)]+)\)", r"[\1](" + WIKI_BASE_URL + r"/\2)", rx2) # Fix map links
        return rx3

    def set_location(self, location_in_html):
        self.location = md(location_in_html.strip().replace(u'\xa0', ' '))

    def write_to_file(self, filename=None):

        if filename is None:
            filename = self.name

        # Create destination directory if it doesn't exist
        if not os.path.exists(CACHE_LOCATION + VAULT_NAME):
            os.mkdir(CACHE_LOCATION + VAULT_NAME)

        f = open(CACHE_LOCATION + VAULT_NAME + filename+'.md', 'w')

        description_style = f"## Description\n\n{self.description}\n"
        image = "![["+self.image.url.split("/")[-1]+"]]"
        location_style = f"## Location\n\n{self.location}\n"
        notes_style = f"## Notes & Tips\n\n{self.notes}\n"
        use_style = f"## Use\n\n{self.use}\n"

        output_str = image + "\n" + description_style + "\n" + location_style + "\n" + use_style + "\n" + notes_style
        
        f.write(output_str)
        f.close()

class Image:
    def __init__(self, url, name=''):
        self.url = url
        self.name = (name if name != '' else self.derive_name_from_url())

    def derive_name_from_url(self):
        return convert_token_to_name(get_url_last_token(self.url))
    
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

### Write to file named after URL

# Get URL's last token
def get_url_last_token(url):
    endpoint = url.split('/')[-1]
    return endpoint

def convert_token_to_name(token):
    return token.replace('+', ' ')

'''
'''
def parse_endpoint_to_entity(url, entity_type=None, force_download_image=False):
    entity_name = convert_token_to_name(url.split("/")[-1])

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
    image_name = image_attr_src.split('/')[-1]
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
    # walk the block for the information
    # Recursive=False is necessary to avoid repeat nested tags
    for element in content_block.find_all(["h3", "p","ul"], recursive=False):
        #print("ELEMENT = ", str(element))
        element_str = str(element)

        # This works by dint of the first element always being this string (guaranteed?)
        if '<h3 class="bonfire">where to find' in element_str.lower():
            mode = 'LOCATION'
        elif 'tips</h3>' in element_str.lower():
            mode = 'NOTES_AND_TIPS'
        elif 'use</h3>' in element_str.lower():
            mode = 'USE'

        if mode == 'LOCATION':
            location_tokens.append(str(element))
        elif mode == 'NOTES_AND_TIPS':
            notes_tokens.append(str(element))
        elif mode == 'USE':
            use_tokens.append(str(element))
    
    # Vagaries of the Notes & Tips section--
    # - Remove paragraphs
    # - Drop last two elements
    notes_tokens = notes_tokens[1:-1]
    if entity_type == EntityType.WEAPON:
        notes_tokens = list(filter(lambda c: c[0:2] != '<p', notes_tokens))[1:-2]
    
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
    #print('\n'.join(map(str,notes_tokens)))

    #print(md(''.join(location_tokens)))

    #s.replace(u'\xa0', ' ')
    # Create Entity parts
    location = ' '.join(location_tokens)#.encode("ascii", "ignore")
    notes = ' '.join(notes_tokens)#.encode("ascii", "ignore")
    use = ' '.join(use_tokens)
    #print(entity_name)

    return Entity(entity_name, url, image=image, description=description, location=location, use=use, notes=notes)

'''
'''
def get_weapons_endpoints(limit=None):
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

'''
'''
def get_items_endpoints(limit=None):
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

'''
'''
def get_all_endpoints():
    endpoints = []
    
    weapons_endpoints = get_weapons_endpoints()
    # print("Weapons Endpoints: a", len(weapons_endpoints))
    # for endpoint in weapons_endpoints:
    #     print(endpoint)
    #     endpoints.append(endpoint)
    endpoints.extend(weapons_endpoints)

    items_endpoints = get_items_endpoints()
    endpoints.extend(items_endpoints)

    return endpoints

# ====================================================

def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    log = logging.getLogger("elden-bring-logger")

    # Create destination directory if it doesn't exist
    if not os.path.exists(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY):
        os.mkdir(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY)

    # all_endpoints = get_all_endpoints()
    all_endpoints = get_weapons_endpoints()
    # all_endpoints = get_items_endpoints()[0:10]

    # List of entities that exhibit parsing issues
    blacklist = ["Miquellan Knight's Sword", "Greataxe"]

    log.info(f"Parsing {len(all_endpoints)} entities...")
    for idx, endpoint in enumerate(all_endpoints):
        entity_name = endpoint.split('/')[-1].replace('+', ' ')
        if entity_name in blacklist:
            continue
        log.info(f"Parsing {entity_name} [{idx+1} of {len(all_endpoints)}]...")
        entity = parse_endpoint_to_entity(endpoint, force_download_image=False)
        entity.write_to_file()

    # item = parse_endpoint_to_entity(WIKI_BASE_URL+"/Dagger", EntityType.WEAPON, force_download_image=False)
    # item = parse_endpoint_to_entity(WIKI_BASE_URL+"/Fingerslayer+Blade", force_download_image=False)
    # item = parse_endpoint_to_entity(WIKI_BASE_URL+"/Miquellan+Knight's+Sword", force_download_image=False)
    # print(item)
    # item.write_to_file()

if __name__=="__main__":
    main()