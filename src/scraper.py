import os

import requests
from bs4 import BeautifulSoup as bs

from constants import *
from objects import *

class Scraper:
    """
    Collection of functions to parse HTML pages into entities.
    """

    # List of entities that exhibit parsing issues due to inconsistency with other similar pages
    weapons_blacklist = ["Miquellan Knight's Sword", "Greataxe"]
    items_blacklist = []
    spells_blacklist = ["Placidusax's Ruin"]
    bosses_blacklist = ["Dragonkin Soldier"]

    # The Legacy Dungeons page is different enough, and there few enough instances, that these can be hardcoded here
    _legacy_dungeons = [
        "/Leyndell+Royal+Capital+(Legacy+Dungeon)", 
        "/Stormveil+Castle", 
        "/Raya+Lucaria+Academy",  
        "/Volcano+Manor", 
        "/Miquella's+Haligtree",
        "/Elphael,+Brace+of+the+Haligtree", 
        "/Crumbling+Farum+Azula", 
    ]

    def __init__(self, logger):
        self.log = logger

    def convert_paths_to_entities(self, paths=[], category=''):
        """
        Convert a list of URLs into entity objects.
        """
        self.log.info(f"Creating {len(paths)} {category} entities...")

        blacklist = self.weapons_blacklist + self.items_blacklist + self.spells_blacklist + self.bosses_blacklist

        entities = []
        for idx, path in enumerate(paths):
            entity_name = path.split('/')[-1].replace('+', ' ')

            if entity_name in blacklist:
                continue

            entity = Entity(entity_name, path, category)

            entities.append(entity)

        return entities

    def get_skill_entities(self):
        """
        Build a list of entities from the table on the Skills page

        This table contains descriptions, so visiting individual Skill pages is not necessary
        """
        url = PATH_SKILLS
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        entities = []
        for row in table_body.find_all('tr'):
            cells = row.find_all('td')
            cells = [ele.text.strip() for ele in cells]
            
            entity_name = cells[0]
            description = cells[5]
            #print(f"{entity_name}")
            entities.append(Entity(entity_name, category='Skills', description=description))
        
        return entities

    def scrape_entity(self, entity, force_image_download=False):
        """
        """
        url = URL_WIKI_BASE + entity.path

        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={"id": "wiki-content-block"})

        # Infobox
        infobox = content_block.find('div', attrs={'class', 'infobox'})

        ## Process the item's main image
        image_tag = infobox.find('img') # First img tag always contains what we want
        image_src = image_tag['src']

        image_name = image_src.split('/')[-1]
        image_url = URL_WIKI_BASE + image_src
        
        image_data = requests.get(image_url).content
        image = Image(image_data, image_name)

        if force_image_download:
            image.write()
        elif ~os.path.isfile(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS + image_name):
            # Download if file does not already exist
            image.write()

        # Throw out all other img tags
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
        upgrades_tokens = []
        # Walk the block for the information
        # Recursive=False is necessary to avoid repeat nested tags
        for element in content_block.find_all(["h3", "p","ul"], recursive=False):
            #print("ELEMENT = ", str(element))
            element_str = str(element).replace(u'\xa0', ' ').strip()
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
            elif 'upgrades in elden ring</h3>' in element_str.lower():
                print("=== MODE SWITCHED TO UPGRADES ===")
                mode = 'UPGRADES'

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
            elif mode == 'UPGRADES':
                upgrades_tokens.append(str(element))
        
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

        entity.image = image
        entity.description = description
        entity.location = location
        entity.use = use
        entity.notes = notes
    
    def get_weapons_urls(self):
        """
        """
        response = requests.get(PATH_WEAPONS)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            urls.append(destination)

        return urls

    def get_shields_urls(self):
        """
        """
        response = requests.get(PATH_SHIELDS)

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

    def get_spirit_ashes_urls(self):
        """
        """
        response = requests.get(PATH_SPIRIT_ASHES)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            urls.append(destination)

        return urls

    def get_items_urls(self):
        """
        Get all Items URLS.

        Several index pages beyond the wiki's Items page must be scraped 
        to account for all items.
        """
        response = requests.get(PATH_ITEMS)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        urls = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            urls.append(destination)
        
        urls = set(urls)    # Unique the values
        
        exclude = {
            "/Interactive+map?id=4605&lat=-93.653126&lng=115.069298&zoom=8&code=mapA",
        }

        urls = urls - exclude   # drop Legacy Dungeons from list

        return list(urls)
    
    def get_talismans_paths(self):
        """
        """
        response = requests.get(PATH_TALISMANS)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        paths = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            paths.append(destination)

        paths = list(set(paths))    # Unique the values

        return paths

    def get_spells_urls(self):
        """
        """
        response = requests.get(PATH_SPELLS)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        paths = []
        for content in content_block.find_all('div', attrs={'class': 'tabcontent 0-tab tabcurrent'}):
            for item in content.find_all('h4', attrs={'style': 'text-align: center;'}):
                for link in item.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
                    destination = link.get('href')
                    paths.append(destination)

        paths = list(set(paths)) # Unique

        return paths

    def get_legacy_dungeons_urls(self):
        return Scraper.legacy_dungeons

    def get_locations_urls(self):
        """
        """
        response = requests.get(PATH_LOCATIONS)

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
        print(Scraper.legacy_dungeons)
        exclude =  set(Scraper.legacy_dungeons + ["/Legacy+Dungeons"])

        urls = urls - exclude   # drop Legacy Dungeons from list

        return list(urls)

    def get_locations_urls(self):
        """
        """
        response = requests.get(PATH_LOCATIONS)

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
        print(Scraper.legacy_dungeons)
        exclude =  set(Scraper.legacy_dungeons + ["/Legacy+Dungeons"])

        urls = urls - exclude   # drop Legacy Dungeons from list

        return list(urls)
    
    def get_bosses_urls(self):
        """
        """
        response = requests.get(PATH_BOSSES)

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

    def get_armor_urls(self):
        """
        """
        response = requests.get(PATH_ARMOR)

        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        urls = []
        
        #TODO

        return urls

    def get_creatures_and_enemies_urls(self):
        """
        """
        response = requests.get(PATH_CREATURES_AND_ENEMIES)

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

    def get_npcs_urls(self):
        """
        """
        response = requests.get(PATH_NPCS)

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