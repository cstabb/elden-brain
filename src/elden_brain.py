import logging
import os
import time
from enum import Enum

from constants import *
from objects import *
from scraper import Scraper

class EldenBrain:
    """
    Render the prima materia
    """

    def __init__(self, logging_enabled=True):

        self.prima_materia = {}

        ## Set up logger
        if logging_enabled:
            logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
            self.log = logging.getLogger('elden-bring-logger')
        else:
            self.log = logging.getLogger('null_logger').addHandler(logging.NullHandler())
        
        self.scraper = Scraper(WIKI_URL, self.log)

        ## Resurrect the brain from existing directories, if they exist
        if os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME):

            # Get existing filenames by category (directory)
            filenames_by_category = {}
            for root, dirs, files in os.walk(LOCAL_CACHE + LOCAL_VAULT_NAME):
                category = root.split('/')[-1]
                assets_location = LOCAL_ASSETS if cfg.remap_assets else LOCAL_ASSETS[0:-1]
                if category in ['', '.obsidian', assets_location]:
                    continue
                else:
                    for filename in files:
                        if category not in filenames_by_category:
                            filenames_by_category[category] = []
                        filenames_by_category[category].append(filename)
            
            # Populate the Prima Materia
            for category, filename in filenames_by_category.items():
                entity = Entity.from_md(filename)

                if category not in self.prima_materia:
                    self.prima_materia[category] = []
                self.prima_materia[category].append(entity)

        ## Create directories if they don't already exist
        if not os.path.exists(LOCAL_CACHE):
            os.mkdir(LOCAL_CACHE)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN)

    def __getitem__(self, category):
         return self.prima_materia[category]

    def create(self, name=None, force_overwrite=False):
        """
        Create the Elden Brain. Scrapes the wiki and generates Markdown documents.

        A single entity's name can be passed in if a specific one is desired.
        Otherwise, this will scrape all pages.
        """

        if name is None or name == '':
            # Make all
            categories = self.getCategories()

            for category in categories:
                self.createByCategory(category)

            return
        else:
            self._prepareEntity()
            
            # scrape
            self.scraper.scrapeEntity()

            # make

            return

    def createByCategory(self, category, force_overwrite=False):
        """
        Create all entities that fall within a known category.
        """

        # Get all names within a category
        self.scraper.getNamesByCategory()

        return

    def getCategories(self):
        """
        Get all known categories as a list.
        """

        categories = []
        for category in Category:
            categories.append(category.value)
        categories.remove(Category.NONE.value)

        return categories

    def getNamesByCategories(self, category):
        return self.scraper.getNamesByCategory(category)

    def add(self, entity):
        if not isinstance(entity, Entity):
            raise TypeError(f'entity {entity} is not an Entity')

    def update_entity_names(self, category=''):
        target = category.value + ".txt"
        # if not os.path.exists(destination)

        paths = self.scraper.get_paths(category)

        f = open(target, 'w')
        for path in paths:
            f.write(path + "\n")
        f.close()

    def create_skills(self, overwrite=True):
        """
        """
        skill_entities = self.scraper.get_skill_entities()

        self.log.info(f"Creating {len(skill_entities)} Skills...")
        
        for idx, skill in enumerate(skill_entities):
            self.log.info(f"Writing {skill.name} [{idx+1} of {len(skill_entities)}]...")
            skill.write()
            time.sleep(0.001)   # Necessary to allow Obsidian a moment to recognize the new file
        
    def create_hidden(self, overwrite=True):
        all_targets = classes + stats + status_effects + armor_type + \
                      spell_type + weapon_type + shield_type + \
                      hide_list + sites_of_grace# + items_to_hide
        destination_path = LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN

        self.log.info(f"Creating {len(all_targets)} hidden files...")

        for idx, target in enumerate(all_targets):
            # Create a new file if it doesn't exist or overwrite is True
            if overwrite or not os.path.isfile(destination_path + target):
                self.log.info(f"Writing {target} hidden file [{idx+1} of {len(all_targets)}]...")
                f = open(destination_path + target + '.md', 'w')
                f.write(HIDDEN_TAG)
                f.close()
                time.sleep(0.001)   # Necessary to allow Obsidian time to recognize the new file

    def _prepareEntity(self, name, category=''):
        """
        If the exact name of an entity is known, it may be used and the path derived.

        Since applying categories to entities would require keeping lists of ALL entities 
        (instead of scraping entity names by category) entities created in this way will 
        be stored in in the 'Unknown' category and write to the same in Obsidian.

        This function is mainly used for debugging; prepare_entities should be used in most cases.
        """
        self.log.info(f"Preparing {name}...")
        
        entity = Entity(name, category=category)

        self.add(entity)

        if category == '':
            if 'Unknown' not in self.prima_materia:
                self.prima_materia['Unknown'] = [entity]
            else:
                self.prima_materia['Unknown'].append(entity)
        else:
            if category not in self.prima_materia:
                self.prima_materia[category] = [entity]
            else:
                self.prima_materia[category].append(entity)
        
        return 

    def _prepareEntities(self, category=''):
        """
        Create the entity objects for a given category.
        """
        paths = self.scraper.get_paths(category)
        
        entities = self.scraper.convert_paths_to_entities(paths, category) # Only URLs and names at this point
        
        self.prima_materia[category] = entities

    def scrape_entity(self, name, category='', write=False):
        """
        """
        self._prepareEntity(name, category)
        # print(len(self.prima_materia[category]))
        # print(self.prima_materia[category][0].name)

        if category == '':
            # If category isn't known, run through all entities to see if name exists
            for known_category, entities in self.prima_materia.items():
                for entity in entities:
                    if entity.name == name:
                        self.scraper.scrapeEntity(entity)
                        if write:
                            entity.write()
        elif category == Category.SKILLS:
            self.log.warning(f"")
        # elif category == EntityCategory.LEGACY_DUNGEONS:
        else:
            for entity in self.prima_materia[category]:
                # print(entity)
                reconstructed_path = "/" + re.sub(r" ", r"+", name) # this is a dumb hack
                # print(entity.path)
                # print(reconstructed_path)
                if entity.path == reconstructed_path:
                    self.log.info(f"Scraping {entity.name}...")
                    if category == Category.LEGACY_DUNGEONS:
                        self.scraper.scrape_legacy_dungeon_entity(entity)
                    else:
                        self.scraper.scrapeEntity(entity)
                    # print(entity)
                    if write:
                        entity.write()
            
    def scrape_entities(self, category='', write=False):
        """
        """
        self._prepareEntities(category)

        # print(self.prima_materia[category])

        if category == '':
            for known_category, entities in self.prima_materia.items():
                if known_category == Category.SKILLS:
                    continue
                self.log.info(f"Scraping {known_category}...")
                for i, entity in enumerate(entities):
                    self.log.info(f"Scraping {entity.name} [{i+1} of {len(self.prima_materia[known_category])}]...")
                    self.scraper.scrapeEntity(entity)
                    if write:
                        entity.write()
        elif category == Category.SKILLS:
            skills_data = self.scraper.scrape_skills_data()
            # print(skills_data["Great Oracular Bubble Skill"])
            skills_data = { name_overrides.get(k, k): v for k, v in skills_data.items() }
            # print(new_dict["Great Oracular Bubble (Skill)"])
            for entity in self.prima_materia[Category.SKILLS]:
                if entity.name in skills_data:
                    # print(f"NAME: {entity.name}\n{skills_data[entity.name]}")
                    entity.content = skills_data[entity.name]
                if write:
                    entity.write()
                    time.sleep(0.001)
        else:
            for i, entity in enumerate(self.prima_materia[category]):
                self.log.info(f"Scraping {entity.name} [{i+1} of {len(self.prima_materia[category])}]...")
                if category == Category.LEGACY_DUNGEONS:
                    # print(entity)
                    self.scraper.scrape_legacy_dungeon_entity(entity)
                    # print(f"CONTENTS===\n{entity.contents}")
                    # print(entity)
                else:
                    self.scraper.scrapeEntity(entity)
                if write:
                    entity.write()

    def write_entity(self, name, category=''):
        """
        """
        self.log.info(f"Writing {name} to markdown file...")

        if category != '':
            for entity in self.prima_materia[category]:
                if entity.name == name:
                    entity.write()
        # If category isn't known, run through all entities to see if name exists
        for known_category, entities in self.prima_materia.items():
            for entity in entities:
                if entity.name == name:
                    entity.write()

    def write_entities(self, category=''):
        """
        """
        self.log.info(f"Writing {category} to markdown files...")

        if category != '':
            for entity in self.prima_materia[category]:
                entity.write()
        else:
            for i, entity in self.prima_materia.items():
                entity.write()

    def get_entity_names(self, category=''):
        """
        """
        #TODO: Check for invalid categories

        if category not in self.prima_materia:
            self.prepare_entities(category)

        entity_names = []
        for entity in self.prima_materia[category]:
            entity_names.append(entity.name)

        entity_names.sort()

        return entity_names
