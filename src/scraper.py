import os

import requests
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString, Tag

from constants import *
from objects import *

class Scraper:
    """
    Collection of functions to parse HTML pages into entities.
    """

    def __init__(self, logger):
        self.log = logger

    def convert_paths_to_entities(self, paths=[], category=''):
        """
        Convert a list of URLs into entity objects.
        """
        self.log.info(f"Creating {len(paths)} {category.value} entities...")

        blacklist = weapons_blacklist + items_blacklist + spells_blacklist + bosses_blacklist

        entities = []
        for idx, path in enumerate(paths):
            entity_name = path.split('/')[-1].replace('+', ' ')

            if entity_name in blacklist:
                continue

            entity = Entity(entity_name, path, category)

            entities.append(entity)

        return entities

    def scrape_skills_data(self):
        """
        Build a list of entities from the table on the Skills page

        This table contains descriptions, so visiting individual Skill pages is not necessary
        """
        response = requests.get(PATH_SKILLS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        skills_data = {}
        for row in table_body.find_all('tr'):
            cells = row.find_all('td')
            cells = [ele.text.strip() for ele in cells]
            name = cells[0]
            description = cells[5]
            #print(f"{entity_name}")
            skills_data[name] = description
        
        return skills_data

    def scrape_legacy_dungeon_entity(self, entity, force_image_download=False):
        """
        """
        target_section_names = [
            "NPCs", 
            "Bosses", 
            "Items", 
            "Enemies"
        ]

        response = requests.get(PATH_LEGACY_DUNGEONS)
        soup = bs(response.text, 'html.parser')

        contents = {}
        this_section = ""
        for col in soup.find_all('div', attrs={'class': 'col-sm-4 col-md-3 col-md-push-9'}):
            for section in col.find_all(['h3', 'a']):
                if section.name == 'h3':
                    for section_name in target_section_names:
                        if section_name in section.string:
                            # Start new section
                            this_section = section_name
                            contents[this_section] = []
                            #print(f"{section.string}\n---------------")
                elif section.name == 'a':
                    link = section.get('href')
                    if this_section != '':
                        contents[this_section].append(link)
                    #print(link)
        
        entity.contents = contents

    def scrape_entity(self, entity, force_image_download=False):
        """
        """
        #print("SCRAPING")
        if entity.category == 'Legacy Dungeons':
            self.scrape_legacy_dungeon(entity, force_image_download)
            return
        
        response = requests.get(URL_WIKI_BASE + entity.path)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Infobox
        infobox = content_block.find('div', attrs={'class', 'infobox'})

        ## Process the item's main image
        image_tag = infobox.find('img') # First img tag always contains what we want
        image_src = image_tag['src']

        image_name = image_src.split('/')[-1]
        image_url = URL_WIKI_BASE + image_src
        
        image_data = requests.get(image_url).content
        image = Image(image_data, image_name)

        if force_image_download or not os.path.isfile(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS + image_name):
            image.write()

        # Throw out all other img tags
        for img in content_block("img"):
            img.decompose()
        # Throw out all span tags
        # for span in content_block("span"):
        #     span.decompose()
        # Throw out all strong tags
        # for img in content_block("strong"):
        #     img.decompose()

        def parse_description(parent, description):
            ems = parent.find_all('em')
            # print(ems)
            for line in ems:
                # print(line.contents)
                values = [str(x).replace("<em>", "") for x in line.contents]
                # print(values)
                for i, val in enumerate(values):
                    # print(repr(val))
                    if val != "<br/>":
                        values[i] = "<em>"+val+"</em>"
                    # else:
                    #     values[i] = " "
                # print(repr(values))
                description += ' '.join(values) + ' '
            if len(ems) > 0:
                description += "<br><br>"
            return description
        
        # Get description
        description = ""
        for item in content_block.find_all('div', attrs={'class', 'lineleft'}):
            # print(f"\n\BLOCK === \n{block}")
            paragraphs = item.find_all('p')
            # if len(paragraphs) == 0:

            if len(paragraphs) == 0:
                description = parse_description(item, description)
            else:
                for paragraph in paragraphs:
                    # print(f"\n\PARAGRAPH === \n{paragraph}")
                    description = parse_description(paragraph, description)
        # print(f"\n\nDESCRIPTION === \n{description}")
        description = description.replace("</em><em>", "").replace("</em><br/><em>", "")
        # description = re.sub(r"<span", r"", description)
        # print(f"\n\nDESCRIPTION === \n{description}")

        # Drop these sections
        sections_to_drop = [
            "Moveset", 
            "Upgrades", 
            "Builds", 
            "Shop", 
            "Combat [Ii]nformation", 
            "Gallery", 
            "Walkthrough", 
            "Map", 
            "GALLERY", 
            "All .*Pieces", 
            # "Boss",
            # "All ", # Final section of armor sets pages (space included to avoid collision with All-Knowing Set)
        ]

        contents = {}

        # TODO: Capture additional headers
        for col in content_block.find_all('h3', attrs={'class': 'bonfire'}):
            #print(f"COLUMN: {str(col)}")
            this_section = str(col)
            contents[this_section] = ""

            # print(this_section)

            for section in col.find_next_siblings(['h3', 'ul', 'ol', 'p', 'div']):
                # print(f"NAME: {str(section.name)}")
                # print(f"SECTION: {str(section.contents)}")
                if section.name in ['h3'] or "Click below for a list of all possible Ashes of War that can be applied" in str(section):
                    break
                else:
                    # print(f"SECTION: {str(section.contents)}")
                    contents[this_section] += str(section)

        # print(f"FIRST\n\n{contents.keys()}\n")
        # eg = contents['<h3 class="bonfire">Flying Dragon Agheel Combat information</h3>']
        # print(f"EXAMPLE===\n{eg}")

        # Find the key of the Drops header
        header_key = ""
        for header, item in contents.items():
            if re.search(r"Drop Rates<\/h3>", header):
                header_key = header
        # print(contents[header_key])

        if header_key in contents:
            table = bs(contents[header_key], 'html.parser') # Re-Soupify
            contents[header_key] = ""   # Clear the value
            for row in table.find_all('tr')[1:]:
                # print(f"ROW ===\n{row}")
                for item in row.find('a'):
                    link = item.string
                    link = re.sub(r"(.+)", r"%BULLET% [[\1|\1]]\n", link)
                    contents[header_key] += link
                    # print(f"LINK ===\n{link}")

        # drop_contents = md(contents[header_key])
        # drop_contents = re.sub(r"\[\[([^\|]+)\|\1", r"[[\1\\|\1", drop_contents)
        # print(f"DROP ===\n{contents[header_key]}")
        # contents[header_key] = drop_contents


        # Drop the undesirable sections from contents
        keys_to_drop = []
        for key in contents:
            for drop_string in sections_to_drop:
                if re.search(drop_string, key):
                    keys_to_drop.append(key)

        for key in keys_to_drop:
            del contents[key]
        
        # print(f"SECOND\n\n{contents}")

        headers = {
            r'<h3 class=\"bonfire\">Where to [F|f]ind[^<]+<\/h3>':      r"### Location\n\n",
            r'<h3 class=\"bonfire\">.+Location in Elden Ring<\/h3>':    r"### Location\n\n",
            r'<h3 class=\"bonfire\">.+Location(s*)<\/h3>':              r"### Location\n\n",
            r'<h3 class=\"bonfire\">.+use in Elden Ring<\/h3>':         r"### Use\n\n",
            r'<h3 class=\"bonfire\">.+Use<\/h3>':                       r"### Use\n\n",
            r'<h3 class=\"bonfire\">.+Note[^<]+<\/h3>':                 r"### Notes\n\n", 
            r'<h3 class=\"bonfire\">.+[Ii]nformation<\/h3>':            r"### Notes\n\n", 
            r'<h3 class=\"bonfire\">.+Build[^<]+<\/h3>':                r"### Builds\n\n", 
            r'<h3 class=\"bonfire\">Dialogue.+<\/h3>':                  r"### Dialogue\n\n",
            r'<h3 class=\"bonfire\">Elden Ring.+Boss<\/h3>':            r"### Boss Information\n\n",
            r'<h3 class=\"bonfire\">Elden Ring.+Boss \((.+)\)<\/h3>':   r"### Boss Information (\1)\n\n",
            r'<h3 class=\"bonfire\">Elden Ring.+Drop Rates<\/h3>':      r"### Drops\n\n",
        }
        
        # Build a string from contents while replacing headers
        # Begin with the description
        contents_string = description
        for key, val in contents.items():
            header = key
            for header_regex, remap in headers.items():
                if re.search(header_regex, key):
                    # print(f"\n\nMAP ===\nHEADER={header_regex}\nREMAP{remap}\nKEY={key}")
                    header = re.sub(header_regex, remap, key)
                    # print(f"MAP AFTER ===\nHEADER={header_regex}\nREMAP{remap}\nKEY={key}")
                    # header = remap

            contents_string += header + val

        contents_string = re.sub(r"\<p\>[\s]+\<\/p\>", r"", contents_string)
        contents_string = re.sub(r"<br\/>", r"<br>", contents_string)

        # print(f"\nTHIRD ===\n{contents_string}")

        entity.image = image
        entity.content = contents_string

    def get_weapons_paths(self):
        """
        """
        response = requests.get(PATH_WEAPONS)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        paths = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            paths.append(destination)

        paths = list(set(paths)) # Unique

        return paths

    def get_shields_paths(self):
        """
        """
        response = requests.get(PATH_SHIELDS)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        paths = []
        for item in content_block.find_all('h4'):
            for link in item.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
                #print(link)
                destination = link.get('href')
                paths.append(destination)

        paths = list(set(paths)) # Unique

        return paths

    def get_spirit_ashes_paths(self):
        """
        """
        response = requests.get(PATH_SPIRIT_ASHES)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        paths = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            paths.append(destination)

        return paths

    def get_items_paths(self):
        """
        Get all Items URLS.

        Several index pages beyond the wiki's Items page must be scraped 
        to account for all items.
        """
        response = requests.get(PATH_ITEMS)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Weapons page
        paths = []
        for item in content_block.find_all('a', attrs={'class': 'wiki_link wiki_tooltip'}):
            destination = item.get('href')
            paths.append(destination)
        
        paths = set(paths)    # Unique the values
        
        exclude = {
            "/Interactive+map?id=4605&lat=-93.653126&lng=115.069298&zoom=8&code=mapA",
        }

        paths = paths - exclude   # drop Legacy Dungeons from list

        return list(paths)
    
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

    def get_spells_paths(self):
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

    def get_legacy_dungeons_paths(self):
        #print(f"===========LEGACY DUNGEONS\n{self.legacy_dungeons}")
        return self.legacy_dungeons

    def get_locations_paths(self):
        """
        """
        response = requests.get(PATH_LOCATIONS)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        paths = []
        for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'row'})):
            for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = link.get('href')
                paths.append(destination)
        print(paths)
        paths = paths[0:-6]   # Last several elements contain throwaway urls
        paths.append("/Three+Sisters")    # Add in anything missing
        paths = set(paths)    # Unique the values
        #print(Scraper.legacy_dungeons)
        exclude =  set(legacy_dungeons + ["/Legacy+Dungeons", "/Torrent+(Spirit+Steed)"])

        paths = paths - exclude   # drop Legacy Dungeons from list

        return list(paths)
    
    def get_bosses_paths(self):
        """
        """
        response = requests.get(PATH_BOSSES)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        paths = []
        for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'tabcontent 0-tab tabcurrent'})):
            for line in row.find_all('li'):
            # for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = line.a.get('href')
                paths.append(destination)

        paths = list(set(paths))    # Unique

        return paths

    def get_armor_paths(self):
        """
        """
        response = requests.get(PATH_ARMOR)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        paths = []
        
        #TODO

        return paths

    def get_creatures_and_enemies_paths(self):
        """
        """
        response = requests.get(PATH_CREATURES_AND_ENEMIES)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main Locations page
        paths = []
        # for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'row'})):
        for col in soup.find_all('div', attrs={'class': 'col-sm-4'}):
            for section in col.find_all(['h3', 'h4']):
                for link in section.find_all('a', attrs={'class': 'wiki_link'}):
                    destination = link.get('href')
                    # print(destination)
                    paths.append(destination)

        # paths = []
        # for row in content_block.find_all('div', attrs={'id': 'reveal'}):
        #     for link in row.find_all('a', attrs={'class': 'wiki_link'}):
        #         destination = link.get('href')
        #         # destination = '/' + destination.split('/')[-1]
        #         paths.append(destination)
        
        paths = set(paths)    # Unique the values
        
        exclude = {
            "/NPC+Invaders", 
        }

        paths = paths - exclude
        
        return list(paths)

    def get_npcs_paths(self):
        """
        """
        response = requests.get(PATH_NPCS)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        # Get all entities from the main NPCs page
        paths = []
        for row in content_block.find_all('div', attrs={'id': 'reveal'}):
            for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = link.get('href')
                destination = '/' + destination.split('/')[-1]
                paths.append(destination)

        # Get all merchants
        response = requests.get(PATH_MERCHANTS)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})
        for row in content_block.find_all('h4'):
            for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                destination = link.get('href')
                paths.append(destination)
        
        exclude = {
            "/Isolated+Merchants", 
            "/Nomadic+Merchants", 
            "/Volcano+Manor+Spirit", 
            "/Merchants#blacksmithing", 
            "/Merchants#equipment", 
            "/Merchants#generalgoods", 
            "/Merchants#special", 
            "/Merchants#spells",
            "/Smithing+Master+Iji", 
            "/Blacksmith+Hewg", 
        }

        paths = set(paths) - exclude   # drop Legacy Dungeons from list

        paths = list(set(paths))    # Unique

        return paths

    def get_skills_paths(self):
        """
        """
        response = requests.get(PATH_SKILLS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        paths = []
        for row in table_body.find_all('tr'):
            for td in row.find('td'):
                #print(td)
                try:
                    path = td.get('href')
                    paths.append(path)
                except AttributeError:
                    pass    # Fail silently on "No Skill" (not a link)
                #print(path)
                # print(td.href)
                # for link in td.find_all('a', attrs={'class': 'wiki_link'}):
                #     path = link.get('href')
                #     path = '/' + path.split('/')[-1]
                #     print(path)
                    # print(td)
            # cells = row.find_all('td')
            # cells = [ele.text.strip() for ele in cells]
            # entity_name = cells[0]
            # paths.append(entity_name)

        paths = list(set(paths))    # Unique
        # print(paths)    
        return paths

    def get_armor_sets_paths(self):
        """
        """
        # Armor Sets
        response = requests.get(PATH_ARMOR)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('div', attrs={'class': 'col-sm-3', 'style': 'float-left: !Important; height: auto;'})

        paths = []
        for link in table_body.find_all('a'):
            path = link.get('href')
            # paths.append(path)
        
        # Helms
        response = requests.get(PATH_ARMOR_HELMS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        for row in table_body.find_all('tr'):
            paths.append(row.a.get('href'))

        # Chest Armor
        response = requests.get(PATH_ARMOR_CHESTS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        for row in table_body.find_all('tr'):
            pass
            # paths.append(row.a.get('href'))

        # Gauntlets
        response = requests.get(PATH_ARMOR_GAUNTLETS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        for row in table_body.find_all('tr'):
            pass
            # paths.append(row.a.get('href'))
        # paths.remove('/Gauntlets')

        # Leg Armor
        response = requests.get(PATH_ARMOR_LEGS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        for row in table_body.find_all('tr'):
            pass
            # paths.append(row.a.get('href'))
        
        paths = list(set(paths))    # Unique

        return paths

    def get_paths(self, category=''):
        """
        """
        # TODO: Blank category means prepare all... maybe ask the user if this is really desired

        if category == EntityCategory.LEGACY_DUNGEONS:
            paths = self.get_legacy_dungeons_paths()
            return paths
        
        # response = requests.get(self.category_paths)

        # soup = bs(response.text, 'html.parser')

        # content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        paths = []
        if category == EntityCategory.BOSSES:
            paths = self.get_bosses_paths()
        elif category == EntityCategory.ENEMIES:
            paths = self.get_creatures_and_enemies_paths()
        elif category == EntityCategory.ITEMS:
            paths = self.get_items_paths()
        elif category == EntityCategory.LEGACY_DUNGEONS:
            paths = self.get_legacy_dungeons_paths()
        elif category == EntityCategory.LOCATIONS:
            paths = self.get_locations_paths()
        elif category == EntityCategory.NPCS:
            paths = self.get_npcs_paths()
        elif category == EntityCategory.SHIELDS:
            paths = self.get_shields_paths()
        elif category == EntityCategory.SKILLS:
            paths = self.get_skills_paths()
        elif category == EntityCategory.SPELLS:
            paths = self.get_spells_paths()
        elif category == EntityCategory.TALISMANS:
            paths = self.get_talismans_paths()
        elif category == EntityCategory.WEAPONS:
            paths = self.get_weapons_paths()
        elif category == EntityCategory.ARMOR:
            paths = self.get_armor_sets_paths()
        
        paths.sort()
        for path in paths:
            print(path)

        return paths