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

    def __init__(self, wiki_url, logger):
        self.wiki_url = wiki_url
        self.log = logger
        self.indexer = self.Indexer(self)

    def convertPathToEntityName(self, path):
        return path.split('/')[-1].replace('+', ' ')

    def convertEntityNameToPath(self, entity_name=''):
        return '/' + entity_name.replace(' ', '+')

    def convertMdToEntityName(self, md_filename=''):
        return re.sub(r'', r'', md_filename)

    def convertMdToPath(self, md_filename=''):
        entity_name = self.convertMdToEntityName(md_filename)
        return self.convertEntityNameToPath(entity_name)

    def getContentBlock(self, url):
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        return content_block

    def convert_paths_to_entities(self, paths=[], category=''):
        """
        Convert a list of URLs into entity objects.
        """
        self.log.info(f"Creating {len(paths)} {category.value} entities...")

        # blacklist = weapons_blacklist + items_blacklist + spells_blacklist + bosses_blacklist

        entities = []
        for idx, path in enumerate(paths):
            entity_name = self.convertPathToEntityName(path)

            # if entity_name in blacklist:
            #     continue

            entity = Entity(entity_name, category=category)

            entities.append(entity)

        entities = list(set(entities))    # Unique the values

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
            # cells = [ele.text.strip() for ele in cells]
            try:
                path = cells[0].a.get('href')
            except:
                path = "/No+Skill"
            # print(f"PATH === {path}")
            name = self.convertPathToEntityName(path)
            description = str(cells[5])
            # print(f"NAME === {name}")
            # print(f"{description}")
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

        # print(URL_WIKI_BASE + entity.path)

        response = requests.get(WIKI_URL + entity.path)
        soup = bs(response.text, 'html.parser')

        contents = {}
        this_section = ""
        for col in soup.find_all('div', attrs={'class': 'col-sm-4 col-md-3 col-md-push-9'}):
            # print(f"\nCOL === \n{col}")
            for section in col.find_all(['h3', 'a']):
                if section.name == 'h3':
                    for section_name in target_section_names:
                        if section_name in section.string:
                            # Start new section
                            this_section = section_name
                            contents[this_section] = []
                            # print(f"{section.string}\n---------------")
                elif section.name == 'a':
                    link = section.get('href')
                    if this_section != '':
                        contents[this_section].append(link)
                    # print(link)
        
        contents_str = ""
        for key, vals in contents.items():
            # print(f"KEY===\n{key}\nVAL===\n{vals}\n\n")
            contents_str += "\n### " + key + "\n\n"
            for val in vals:
                val = re.sub(r"\+", r" ", val)
                val = re.sub(r"[\/\n]", r"", val)
                val = re.sub(r"(.+)", r"[[\1|\1]]", val)
                contents_str += "%BULLET% " + val + "\n"

        # print(f"{contents_str}")
        
        entity.content = contents_str

    def scrapeEntity(self, entity, force_image_download=False):
        """
        """
        if entity.category == Category.LEGACY_DUNGEONS:
            self.scrape_legacy_dungeon(entity, force_image_download)
        
        path = WIKI_URL + entity.path
        response = requests.get(path)
        if response.status_code == 404:
            self.log.error(f"404 PAGE NOT FOUND - {path}")
            raise SystemExit
        soup = bs(response.text, 'html.parser')
        
        content_block = soup.find('div', attrs={'id': 'wiki-content-block'})
        content_block.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
        # nonBreakSpace = 
        # soup = content_block.replace(u'\xa0', ' ')

        # print(content_block)
        # Infobox
        if entity.name == "Miquellan Knight's Sword":
            infobox = content_block.find('li', attrs={'class', 'infobox'})
        else:
            infobox = content_block.find('div', attrs={'class', 'infobox'})

        ## Process the item's main image
        image = None
        try:
            image_tag = infobox.find('img') # First img tag always contains what we want
            image_src = image_tag['src']

            image_name = image_src.split('/')[-1]
            if "discordapp" in image_src:
                image_url = image_src
            else:
                image_url = WIKI_URL + image_src
            image_data = requests.get(image_url).content
            image = Image(image_data, image_name)

            if force_image_download or not os.path.isfile(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS + image_name):
                image.write()
        except:
            pass

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
            "Build", 
            "Shop", 
            "Combat [Ii]nformation", 
            "Gallery", 
            "Walkthrough", 
            "Map", 
            "Guide", 
            "GALLERY", 
            "All .*Pieces", 
            # "Boss",
            # "All ", # Final section of armor sets pages (space included to avoid collision with All-Knowing Set)
        ]

        contents = {}

        # TODO: Capture additional headers
        for col in content_block.find_all('h3', attrs={'class': 'bonfire'}):
            #print(f"COLUMN: {str(col)}")
            this_section = re.sub(u'\xa0', ' ', str(col))
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
        keys_to_drop = list(set(keys_to_drop))
        
        for key in keys_to_drop:
            del contents[key]
        
        # print(f"SECOND\n\n{contents}")

        headers = {
            r'<h3 class=\"bonfire\">[Ww]here to [Ff]ind[^<]+<\/h3>':        r"## Location\n\n",
            r'<h3 class=\"bonfire\">.+[Ll]ocation in Elden Ring<\/h3>':     r"## Location\n\n",
            r'<h3 class=\"bonfire\">.+[Ll]ocation(s*)<\/h3>':               r"## Location\n\n",
            r'<h3 class=\"bonfire\">.+[Uu]se in Elden Ring<\/h3>':          r"## Use\n\n",
            r'<h3 class=\"bonfire\">.+[Uu]se<\/h3>':                        r"## Use\n\n",
            r'<h3 class=\"bonfire\">.+[Nn]ote[^<]+<\/h3>':                  r"## Notes\n\n", 
            r'<h3 class=\"bonfire\">.+[Cc]ombat [Ii]nformation<\/h3>':      r"## Combat Information\n\n", 
            r'<h3 class=\"bonfire\">.+(?<!Combat) [Ii]nformation( in Elden Ring)*<\/h3>':    r"## Information\n\n", 
            # r"<h3 class=\"bonfire\">Goldmask Information.+<\/h3>":    r"## Information\n\n", 
            # r'<h3 class=\"bonfire\">.+[Ii]nformation<\/h3>':                r"## Notes\n\n", 
            r'<h3 class=\"bonfire\">.+[Bb]uild[^<]+<\/h3>':                 r"## Builds\n\n", 
            r'<h3 class=\"bonfire\">[Dd]ialogue.+<\/h3>':                   r"## Dialogue\n\n",
            r'<h3 class=\"bonfire\">Elden Ring.+[Bb]oss<\/h3>':             r"## Boss Information\n\n",
            r'<h3 class=\"bonfire\">Elden Ring.+[Bb]oss \((.+)\)<\/h3>':    r"## Boss Information (\1)\n\n",
            r'<h3 class=\"bonfire\">Elden Ring.+[Dd]rop [Rr]ates<\/h3>':    r"## Drops\n\n",
            r'<h3 class=\"bonfire\">Elden Ring.+[Dd]rops<\/h3>':            r"## Drops\n\n",
            r'<h3 class=\"bonfire\">.+[Qq]uest<\/h3>':                      r"## Quest\n\n",
            r'<h3 class=\"bonfire\">.+[Ss]et [Aa]rmor [Pp]ieces[^<]+<\/h3>':    r"## Set Armor Pieces\n\n",
            r'<h3 class=\"bonfire\">.+[Ss]et [Pp]ieces[^<]+<\/h3>':         r"## Set Pieces\n\n",
            r'<h3 class=\"bonfire\">.+[Ss]et in Elden Ring<\/h3>':          r"## Set Information\n\n",
            r'<h3 class=\"bonfire\">.+Creatures, Enemies, and Bosses<\/h3>':    r"## Creatures, Enemies, and Bosses\n\n",
            r'<h3 class=\"bonfire\">.+All Items.+<\/h3>':                     r"## Items\n\n",
            r'<h3 class=\"bonfire\">.+All NPCs and Merchants.+<\/h3>':        r"## NPCs and Merchants\n\n",
        }
        
        # Build a string from contents while replacing headers
        # Begin with the description
        contents_string = description
        for key, val in contents.items():
            header = key
            # print(f"BEFORE === {header}")
            for header_regex, remap in headers.items():
                # print(f"HEADER_REGEX === {header_regex}")
                # print(f"KEY === {key.lower()}")
                if re.search(header_regex, key):
                    # print(f"\n\nMAP ===\nHEADER={header_regex}\nREMAP{remap}\nKEY={key}")
                    header = re.sub(header_regex, remap, key)
                    # print(f"MAP AFTER ===\nHEADER={header_regex}\nREMAP{remap}\nKEY={key}")
                    # header = remap
            # print(f"AFTER === {header}")
            contents_string += header + val# + "\n---\n\n"

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
                for link in item.find_all('a', attrs={'class': 'wiki_link'}):
                    destination = link.get('href')
                    paths.append(destination)

        paths = list(set(paths)) # Unique

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

        additions = [
            "/No+Skill", 
        ]

        paths += additions

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
            paths.append(path)
        
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
            # pass
            paths.append(row.a.get('href'))

        # Gauntlets
        response = requests.get(PATH_ARMOR_GAUNTLETS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        for row in table_body.find_all('tr'):
            # pass
            paths.append(row.a.get('href'))
        # paths.remove('/Gauntlets')

        # Leg Armor
        response = requests.get(PATH_ARMOR_LEGS)
        soup = bs(response.text, 'html.parser')

        table_body = soup.find('tbody')

        for row in table_body.find_all('tr'):
            # pass
            paths.append(row.a.get('href'))
        
        additions = [
            "/Perfumer+Traveler's+Set", 
            "/Nox+Monk+Greaves", 
            "/Nox+Monk+Bracelets", 
            "/Ragged+Set", 
            "/Brave's+Set", 
            "/Deathbed+Set", 
        ]

        paths += additions

        exclude = {
            "/Gauntlets", 
        }

        paths = set(paths) - exclude   # drop Legacy Dungeons from list
        
        paths = list(set(paths))    # Unique

        return paths

    def get_paths(self, category=''):
        """
        """
        # TODO: Blank category means prepare all... maybe ask the user if this is really desired

        if category == Category.LEGACY_DUNGEONS:
            paths = self.get_legacy_dungeons_paths()
            return paths
        
        # response = requests.get(self.category_paths)

        # soup = bs(response.text, 'html.parser')

        # content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

        paths = []
        if category == Category.BOSSES:
            paths = self.get_bosses_paths()
        elif category == Category.ENEMIES:
            paths = self.get_creatures_and_enemies_paths()
        elif category == Category.ITEMS:
            paths = self.get_items_paths()
        elif category == Category.LEGACY_DUNGEONS:
            paths = self.get_legacy_dungeons_paths()
        elif category == Category.LOCATIONS:
            paths = self.get_locations_paths()
        elif category == Category.NPCS:
            paths = self.get_npcs_paths()
        elif category == Category.SHIELDS:
            paths = self.get_shields_paths()
        elif category == Category.SKILLS:
            paths = self.get_skills_paths()
        elif category == Category.SPELLS:
            paths = self.get_spells_paths()
        elif category == Category.TALISMANS:
            paths = self.get_talismans_paths()
        elif category == Category.WEAPONS:
            paths = self.get_weapons_paths()
        elif category == Category.ARMOR:
            paths = self.get_armor_sets_paths()
        elif category == Category.SPIRIT_ASH:
            paths = self.get_spirit_ashes_paths()
        
        paths.sort()
        print('\n'.join(paths))

        return paths

    class Indexer:
        """
        Read index pages to generate lists of entities.
        """

        def __init__(self, outer_class):
            self.scraper = outer_class

        def getNamesForBosses(self):
            content_block = self.scraper.getContentBlock(PATH_BOSSES)

            names = []

            for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'tabcontent 0-tab tabcurrent'})):
                for ul in row.find_all('ul'):
                    for line in ul.find_all('li'):
                        for link in line.find_all('a', attrs={'class': 'wiki_link'}):
                            destination = self.scraper.convertPathToEntityName(link.get('href'))
                            names.append(destination)
        
            exclusions = {
                "Caelid", 
                "Liurnia", 
                "Dragonbarrow", 
                "Impaler's Catacombs", 
                "Stormfoot Catacombs", 
                "Sage's Cave", 
            }

            names = list(set(names) - exclusions)

            names_by_category = {}
            names_by_category[Category.BOSSES.value] = names

            return names_by_category
        
        def getNamesForCreaturesAndEnemies(self):
            content_block = self.scraper.getContentBlock(PATH_CREATURES_AND_ENEMIES)

            names = []
            
            for col in content_block.find_all('div', attrs={'class': 'col-sm-4'}):
                for section in col.find_all(['h3', 'h4']):
                    for link in section.find_all('a', attrs={'class': 'wiki_link'}):
                        destination = self.scraper.convertPathToEntityName(link.get('href'))
                        names.append(destination)

            additions = [
                "Tanith's Knight", 
                "Necromancer", 
                "Skeletons", 
                "Slug", 
                "First-Generation Albinauric", 
                "Second-Generation Albinauric", 
                "Bloody Finger Okina", 
                "Lesser Sanguine Noble", 
                "Giant Skeleton (Spirit)", 
                "Redmane Knight", 
                "Large Oracle Envoy", 
                "Man-Serpent Sorcerer", 
                "Silver Sphere", 
            ]

            names += additions

            exclusions = {
                "NPC Invaders", 
                "Scarlet Rot Zombie", 
            }

            names = list(set(names) - exclusions)
            
            names_by_category = {}
            names_by_category[Category.ENEMIES.value] = names

            return names_by_category

        def getNamesForItems(self):
            """
            Get all Items names.

            Several subcategory index pages beyond the wiki's Items page must be scraped 
            to account for all items.
            """

            def getNamesByItemSubCategory(subcategory):
                path = item_subcategory_paths[subcategory]
                response = requests.get(path)
                soup = bs(response.text, 'html.parser')

                if subcategory in [ItemSubcategory.UPGRADE_MATERIALS, ItemSubcategory.ARROWS_AND_BOLTS]:
                    content_block = soup.find_all('table', attrs={'data-key': 'jumbo'})[0]
                elif subcategory == ItemSubcategory.GREAT_RUNES:
                    content_block = soup.find_all('div', attrs={'class': 'tabcontent 0-tab tabcurrent'})
                else:
                    content_block = soup.find('table')

                names = []

                if subcategory == ItemSubcategory.GREAT_RUNES:
                    for row in content_block:
                        for link in row.find_all('a'):
                            name = link.get('href')
                            if name is not None:
                                names.append(self.scraper.convertPathToEntityName(name))
                else:
                    for row in content_block.find_all('tr'):
                        cells = row.find('td')
                        try:
                            name = cells.a.get('href')
                            names.append(self.scraper.convertPathToEntityName(name))
                        except:
                            pass    # Fail silently

                return names

            names_by_category = {}

            names_by_category[Category.ITEMS.value] = {}

            names_items = names_by_category[Category.ITEMS.value]
            names_items[ItemSubcategory.KEY_ITEMS.value] = []
            names_items[ItemSubcategory.KEY_ITEMS.value] += getNamesByItemSubCategory(ItemSubcategory.KEY_ITEMS)
            names_items[ItemSubcategory.ARROWS_AND_BOLTS.value] = []
            names_items[ItemSubcategory.ARROWS_AND_BOLTS.value] = getNamesByItemSubCategory(ItemSubcategory.ARROWS_AND_BOLTS)
            names_items[ItemSubcategory.BELL_BEARINGS.value] = []
            names_items[ItemSubcategory.BELL_BEARINGS.value] = getNamesByItemSubCategory(ItemSubcategory.BELL_BEARINGS)
            names_items[ItemSubcategory.COOKBOOKS.value] = []
            names_items[ItemSubcategory.COOKBOOKS.value] = getNamesByItemSubCategory(ItemSubcategory.COOKBOOKS)
            names_items[ItemSubcategory.CONSUMABLES.value] = []
            names_items[ItemSubcategory.CONSUMABLES.value] = getNamesByItemSubCategory(ItemSubcategory.CONSUMABLES)
            names_items[ItemSubcategory.CRAFTING_MATERIALS.value] = []
            names_items[ItemSubcategory.CRAFTING_MATERIALS.value] = getNamesByItemSubCategory(ItemSubcategory.CRAFTING_MATERIALS)
            names_items[ItemSubcategory.CRYSTAL_TEARS.value] = []
            names_items[ItemSubcategory.CRYSTAL_TEARS.value] = getNamesByItemSubCategory(ItemSubcategory.CRYSTAL_TEARS)
            names_items[ItemSubcategory.GREAT_RUNES.value] = []
            names_items[ItemSubcategory.GREAT_RUNES.value] = getNamesByItemSubCategory(ItemSubcategory.GREAT_RUNES)
            names_items[ItemSubcategory.INFO_ITEMS.value] = []
            names_items[ItemSubcategory.INFO_ITEMS.value] = getNamesByItemSubCategory(ItemSubcategory.INFO_ITEMS)
            names_items[ItemSubcategory.MULTIPLAYER_ITEMS.value] = []
            names_items[ItemSubcategory.MULTIPLAYER_ITEMS.value] = getNamesByItemSubCategory(ItemSubcategory.MULTIPLAYER_ITEMS)
            names_items[ItemSubcategory.REMEMBRANCE.value] = []
            names_items[ItemSubcategory.REMEMBRANCE.value] = getNamesByItemSubCategory(ItemSubcategory.REMEMBRANCE)
            names_items[ItemSubcategory.TOOLS.value] = []
            names_items[ItemSubcategory.TOOLS.value] = getNamesByItemSubCategory(ItemSubcategory.TOOLS)
            names_items[ItemSubcategory.WHETBLADES.value] = []
            names_items[ItemSubcategory.WHETBLADES.value] = getNamesByItemSubCategory(ItemSubcategory.WHETBLADES)
            names_items[ItemSubcategory.UPGRADE_MATERIALS.value] = []
            names_items[ItemSubcategory.UPGRADE_MATERIALS.value] = getNamesByItemSubCategory(ItemSubcategory.UPGRADE_MATERIALS)

            exclusions = {
                "/Interactive+map?id=4605&lat=-93.653126&lng=115.069298&zoom=8&code=mapA",
                "Caria Manor", 
                "Lesser Kindred of Rot (Pests)", 
                "Merchants", 
                "Torches"
            }

            for key, val in names_by_category.items():
                if key == Category.ITEMS.value:
                    continue
                val = list(set(val) - exclusions)

            return names_by_category

        def getNamesForLegacyDungeons(self):
            names_by_category = {}
            names_by_category[Category.LEGACY_DUNGEONS.value] = LEGACY_DUNGEONS_LIST
            return names_by_category

        def getNamesForLocations(self):
            """
            """
            content_block = self.scraper.getContentBlock(PATH_LOCATIONS)

            names = []

            for idx, row in enumerate(content_block.find_all('div', attrs={'class': 'row'})):
                for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                    destination = self.scraper.convertPathToEntityName(link.get('href'))
                    names.append(self.scraper.convertPathToEntityName(destination))
            
            names = names[0:-6]   # Last several elements contain throwaway urls

            additions = [
                "Three Sisters", 
                "Uld Palace Ruins", 
            ]

            names += additions

            exclusions = set([
                "Torrent (Spirit+Steed)", 
                "Wardead Catacombs", 
            ] + LEGACY_DUNGEONS_LIST)

            names = list(set(names) - exclusions)

            names_by_category = {}
            names_by_category[Category.LOCATIONS.value] = names

            return names_by_category

        def getNamesForNpcs(self):
            """
            """
            response = requests.get(PATH_NPCS)
            soup = bs(response.text, 'html.parser')

            content_block = soup.find('div', attrs={'id': 'wiki-content-block'})

            names = []

            # Get entities from the NPCs page list
            for row in content_block.find_all('div', attrs={'class': 'col-sm-4'}):
                destination = self.scraper.convertPathToEntityName(row.a.get('href'))
                names.append(destination)
                print(f"NPCS LIST = {destination}")

            # Get entities from the NPCs page tag cloud
            for row in content_block.find_all('div', attrs={'id': 'reveal'}):
                for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                    destination = link.get('href')
                    destination = self.scraper.convertPathToEntityName(destination.split('/')[-1])
                    names.append(destination)
                    print(f"NPCS TAG = {destination}")

            # Get all merchants
            response = requests.get(PATH_MERCHANTS)
            soup = bs(response.text, 'html.parser')

            for img in soup("img"):
                img.decompose()

            content_block = soup.find('div', attrs={'id': 'wiki-content-block'})
            for row in content_block.find_all('h4'):
                for link in row.find_all('a', attrs={'class': 'wiki_link'}):
                    # print(f"{link}")
                    destination = self.scraper.convertPathToEntityName(link.get('href'))
                    names.append(destination)
                    print(f"NPCS MERCHANTS = {destination}")
            
            additions = [
                "Torrent (Spirit Steed)", 
                "Volcano Manor Spirit", 
                "Eleonora, Violet Bloody Finger", 
                "Two Fingers", 
            ]

            names += additions

            exclusions = {
                "Isolated Merchants", 
                "Nomadic Merchants", 
                "Nomadic Merchant Mohgwyn Palace", 
                "Volcano Manor Spirit", 
                "Merchants#blacksmithing", 
                "Merchants#equipment", 
                "Merchants#generalgoods", 
                "Merchants#special", 
                "Merchants#spells",
                "Smithing Master Iji", 
                "Blacksmith Hewg", 
                "Miriel Pastor of Vows",   # This one's redundant as 'Miriel, Pastor of Vows' is included in the scrape
            }

            names = list(set(names) - exclusions)

            names_by_category = {}
            names_by_category[Category.NPCS.value] = names

            return names_by_category

        def getNamesByCategory(self, category):

            names_by_category = {}

            def getNamesFunction(category):
                name_function = None

                if category == Category.BOSSES.value:
                    name_function = self.getNamesForBosses
                elif category == Category.ENEMIES.value:
                    name_function = self.getNamesForCreaturesAndEnemies
                elif category == Category.ITEMS.value:
                    name_function = self.getNamesForItems
                elif category == Category.LEGACY_DUNGEONS.value:
                    name_function  = self.getNamesForLegacyDungeons
                elif category == Category.LOCATIONS.value:
                    name_function = self.getNamesForLocations
                elif category == Category.NPCS.value:
                    name_function = self.getNamesForNpcs
                # elif category == Category.SHIELDS.value:
                #     names = self.get_shields_names()
                # elif category == Category.SKILLS.value:
                #     names = self.get_skills_names()
                # elif category == Category.SPELLS.value:
                #     names = self.get_spells_names()
                # elif category == Category.TALISMANS.value:
                #     names = self.get_talismans_names()
                # elif category == Category.WEAPONS.value:
                #     names = self.get_weapons_names()
                # elif category == Category.ARMOR.value:
                #     names = self.get_armor_sets_names()
                # elif category == Category.SPIRIT_ASH.value:
                #     names = self.get_spirit_ashes_names()

                return name_function

            names_by_category = getNamesFunction(category)()
            
            return names_by_category

    def getNamesByCategory(self, category):
        """
        Returns a dictionary? of (potentially nested) categories and lists of names
        """
        return self.indexer.getNamesByCategory(category)

        