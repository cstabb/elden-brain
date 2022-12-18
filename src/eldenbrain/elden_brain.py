import logging
import os
import time
from enum import Enum

from markdownify import markdownify as md
import flatdict

from constants import *
from objects import *
from scraper import Scraper
from text_handling import Formatter


class EldenBrain:
    """
    Render the prima materia.
    """

    def __init__(self, logging_enabled=True):
        ## Set up the logger
        if logging_enabled:
            logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
            self.log = logging.getLogger('elden-bring-logger')
        else:
            self.log = logging.getLogger('null_logger').addHandler(logging.NullHandler())
        
        ## Set up the scraper
        self.scraper = Scraper(WIKI_URL, self.log)

        ## Create directories if they don't already exist
        if not os.path.exists(LOCAL_CACHE):
            os.mkdir(LOCAL_CACHE)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN)

    def getCategories(self):
        """
        Get all known categories as a list.
        """
        categories = []
        for category in Category:
            categories.append(category.value)

        return categories

    def getNamesByCategory(self, category):
        """
        Get a list of names within a known category by scraping its index page(s).
        """
        return self.scraper.getNamesByCategory(category)

    def create(self, name='', category='', force_overwrite=False):
        """
        Create the Elden Brain. Scrapes the wiki and generates Markdown documents.

        A single entity's name can be passed in if a specific one is desired.
        Otherwise, this will scrape all entities.
        """
        if name == '':
            categories = []
            if category != '':
                categories.append(category)
            else:
                categories += self.getCategories()
            for category in categories:
                self._createByCategory(category)
        else:
            self._createEntity(name, category)

    def _createByCategory(self, category):
        """
        Create all entities that fall within a known category.
        """
        self.log.info(f"Creating all pages in the {category} category...")

        if category == 'Skills':
            self._createSkills()
        elif category == 'Hidden':
            self._createHidden()
        else:
            category_tree = self.scraper.getNamesByCategory(category)

            fd =  dict(flatdict.FlatDict(category_tree, delimiter='/'))

            for category, names in fd.items():
                for name in names:
                    self._createEntity(name, category)

    def _createEntity(self, name, category=''):
        """
        Create an entity, scrape its contents, and write it to disk.

        If category is not known, as in the case of a one-off create(), the entity 
        is written to the Vault's top level.
        """
        self.log.info(f"Creating {name}...")

        entity = Entity(name, category=category)
        self.scraper.scrape(entity)
        entity.write()

    def _createSkills(self, overwrite=True):
        """
        Create and scrape Skills entities.

        This is done separately from other categories since all Skills data is 
        scraped from a single page.
        """
        skills_data = self.scraper.scrapeSkills()

        skills = []
        for name, data in skills_data.items():
            entity = Entity(name, category = Category.SKILLS.value)
            entity.content = data
            skills.append(entity)

        self.log.info(f"Creating {len(skills)} Skills...")
        
        for idx, skill in enumerate(skills):
            self.log.info(f"Writing {skill.name} [{idx+1} of {len(skills)}]...")
            skill.write()
            time.sleep(0.001)   # Necessary to allow Obsidian a moment to recognize the new file
        
    def _createHidden(self, overwrite=True):
        """
        Create files in the Hidden folder with the #Hidden tag.

        Many scraped pages link to pages that don't exist, are malforned or misnamed, 
        are not useful, or otherwise should be ignored. These show in Obsidian's 
        graph view as gray, "dead" nodes. By creating these pages and applying 
        the #Hidden tag, they can be suppressed in the graph view with the filter

            -tag:#Hidden
        """
        path = LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN

        self.log.info(f"Creating {len(HIDDEN_LIST)} hidden files...")

        for idx, target in enumerate(HIDDEN_LIST):
            if overwrite or not os.path.isfile(path + target):
                self.log.info(f"Writing {target} hidden file [{idx+1} of {len(HIDDEN_LIST)}]...")

                f = open(path + target + '.md', 'w')
                f.write(HIDDEN_TAG)
                f.close()

                time.sleep(0.001)   # Necessary to allow Obsidian time to recognize the new file

    def _checkCategory(self, category):
        # Check if category is valid
        valid_categories = [category.value for category in Category] + ['']
        if category not in valid_categories:
            raise ValueError('Invalid category, use getCategories() to see valid categories')


class Entity:
    def __init__(self, name, category='', image=None):
        self.path = '/' + name.replace(' ', '+')    # Set the original path before we potentially override name
        
        # Apply name overrides on assignment
        try:
            name = name_overrides[name]
        except KeyError:
            pass
        self.name = name
        
        self.category = category
        self.image = image

        self.tags = []
        if self.category != '':
            self.tags += [re.sub(r' +', r'', category) for category in category.split('/')]

        # Hide 'About' items
        if re.search(r'^About ', self.name):
            self.addTag('Hidden')
        
        self.content = ''
        
    def __str__(self):
        name_f_string = f'\n{self.name}\n========\n\n'
        content_f_string = f'{self.content}'
        return name_f_string + content_f_string
    
    def __setattr__(self, name, value):
        if name == 'content':
            if value == '':
                self.__dict__[name] = value
                return

            text = value

            ## Pre-markdown fixes
            text = Formatter.applyPreMarkdownFixes(text)

            ## Markdownify
            markdown = md(text)

            ## Fixes, and they ain't pretty
            if self.category not in [Category.ARMOR.value]:
                markdown = Formatter.removeNotesAfterSellValue(markdown)

            if self.category in [Category.NPCS.value]:
                markdown = Formatter.cleanDialogue(markdown)

            markdown = Formatter.applyCharacterFixes(markdown)
            markdown = Formatter.applyTextFixes(markdown)

            # Targeted corrections
            markdown = Formatter.applyTargetedCorrections(self.name, markdown)

            self.__dict__[name] = markdown
        else:
            self.__dict__[name] = value

    def addImage(self, name, data):
        self.image = Image(name, data)
        
    def addTag(self, tag):
        tag = re.sub(r' +', r'', tag)
        if tag not in self.tags:
            self.tags.append(tag)

    def setLocation(self, location_in_html):
        self.location = md(location_in_html.strip().replace(u'\xa0', ' '))

    def write(self, additional_tags=[], filename=None):

        if filename is None:
            filename = re.sub(r'\:', r' -', self.name)

        path = LOCAL_CACHE + LOCAL_VAULT_NAME
        if self.category != '':
            path += self.category + '/'

        # Create destination directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        tags_md_string = ''
        if self.tags:
            tags = ['#'+tag for tag in self.tags]
            tags_md_string = ' '.join(tags) + f'\n\n'

        image = ''
        if self.image is not None:
            image = '![['+self.image.name+']]\n\n'

        content_md_string = ''
        if self.content != '':
            content_md_string = f'{self.content}'

        output_str = tags_md_string + image + content_md_string

        # Write the associated image, if it doesn't exist
        try:
            if not os.path.isfile(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS + self.image.name):
                self.image.write()
        except AttributeError:
            pass    # Image doesn't exist
        
        f = open(path + filename+'.md', 'w')
        f.write(output_str)
        f.close()
        

class Image:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    
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
