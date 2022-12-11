import logging
import os
import time
from enum import Enum

from markdownify import markdownify as md

from constants import *
from objects import *
from scraper import Scraper
from text_handling import Formatter


class EldenBrain:
    """
    Render the prima materia.
    """

    def __init__(self, logging_enabled=True):

        self.prima_materia = {}

        ## Set up the logger
        if logging_enabled:
            logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
            self.log = logging.getLogger('elden-bring-logger')
        else:
            self.log = logging.getLogger('null_logger').addHandler(logging.NullHandler())
        
        ## Set up the scraper
        self.scraper = Scraper(WIKI_URL, self.log)

        ## Resurrect the prima materia from existing directories, if they exist
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
            # Populate the prima materia
            for category, filename in filenames_by_category.items():
                entity = Entity.fromMd(filename)
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

    def create(self, name='', force_overwrite=False):
        """
        Create the Elden Brain. Scrapes the wiki and generates Markdown documents.

        A single entity's name can be passed in if a specific one is desired.
        Otherwise, this will scrape all entities.
        """
        if name == '':
            self._createHidden()
            self._createSkills()
            
            categories = self.getCategories()

            for category in categories:
                self.createByCategory(category)
        else:
            entity = self._createEntity(name, category)
            self.scraper.scrape(entity)

    def createByCategory(self, category, force_overwrite=False):
        """
        Create all entities that fall within a known category.
        """
        if category == 'Skills':
            self._createSkills()
        elif category == 'Hidden':
            self._createHidden()
        else:
            names = self.scraper.getNamesByCategory()
            names.remove('Skills')
            for name in names:
                entity = self._createEntity(name, category)
                self.scraper.scrape(entity)

    def _createEntity(self, name, category=''):
        """
        If the exact name of an entity is known, it may be used and the path derived.

        Since applying categories to entities would require keeping lists of ALL entities 
        (instead of scraping entity names by category) entities created in this way will 
        be stored in in the 'Unknown' category and write to the same in Obsidian.

        This function is mainly used for debugging; prepare_entities should be used in most cases.
        """
        self.log.info(f"Creating {name} entity...")
        
        entity = Entity(name, category=category)

        self._add(entity)

        return entity
    
    def getCategories(self):
        """
        Get all known categories as a list.
        """
        categories = []
        for category in Category:
            categories.append(category.value)
        categories.remove(Category.NONE.value)
        categories.remove(Category.SKILLS.value)
        categories.remove(Category.HIDDEN.value)

        return categories

    def getNamesByCategories(self, category):
        """
        Get a list of names within a known category by scraping its index page(s).
        """
        return self.scraper.getNamesByCategory(category)

    def _add(self, entity):
        """
        Add an entity to the prima materia.
        """
        if not isinstance(entity, Entity):
            raise TypeError(f'entity {entity} is not an Entity')

        if entity.category == Category.NONE or entity.category == '' or entity.category is None:
            if 'Unknown' not in self.prima_materia:
                self.prima_materia['Unknown'] = [entity]
            else:
                self.prima_materia['Unknown'].append(entity)
        else:
            if entity.category not in self.prima_materia:
                self.prima_materia[entity.category] = []
            self.prima_materia[entity.category].append(entity)

    def _createSkills(self, overwrite=True):
        """
        Create and scrape Skills entities.

        This is done separate from other categories since all Skills data is scrape from a single page.
        """
        skills_data = self.scraper.scrapeSkills()

        for name, data in skills_data.items():
            entity = Entity(name, category = Category.SKILLS.value, content=data)
            self._add(entity)

        num_skills = len(self.prima_materia[Category.SKILLS.value])

        self.log.info(f"Creating {num_skills} Skills...")
        
        counter = 1
        for category, skill in enumerate(self.prima_materia[Category.SKILLS.value]):
            self.log.info(f"Writing {skill.name} [{counter} of {num_skills}]...")
            counter += 1
            skill.write()
            time.sleep(0.001)   # Allow Obsidian a moment to recognize the new file
        
    def _createHidden(self, overwrite=True):
        """
        Create files in the Hidden folder with the #Hidden tag.

        Many scraped pages link to pages that don't exist, are malforned or misnamed, 
        are not useful, or otherwise should be ignored. Pages with the #Hidden tag 
        can be suppressed in Obsidian's graph view and avoid showing up as dead-end gray nodes.
        """

        path = LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN

        self.log.info(f"Creating {len(all_targets)} hidden files...")

        for idx, target in enumerate(HIDDEN_LIST):
            if overwrite or not os.path.isfile(path + target):
                self.log.info(f"Writing {target} hidden file [{idx+1} of {len(all_targets)}]...")

                f = open(path + target + '.md', 'w')
                f.write(HIDDEN_TAG)
                f.close()

                time.sleep(0.001)   # Necessary to allow Obsidian time to recognize the new file


class Entity:
    def __init__(self, name, category=Category.NONE, image=None):
        self.path = '/' + name.replace(' ', '+')    # Set the original path before we potentially remap name
        
        try:
            name = name_overrides[name]
        except KeyError:
            pass
        self.name = name
        
        self.category = category
        self.image = image

        self.tags = []
        if category != Category.NONE:
            self.tags.append(re.sub(r' +', r'', category.value))

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

            ## Pre-Markdownify modifications
            # text = Formatter.prep_varre_e(text)

            ## Markdownify
            markdown = md(text)

            ## Fixes, and they ain't pretty
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

            # Unify inconsistent links/names
            markdown = Formatter.unify_alexander(markdown)
            markdown = Formatter.unify_boc(markdown)
            markdown = Formatter.unify_imp(markdown)

            markdown = Formatter.unify_astel(markdown)
            markdown = Formatter.unify_putrid_corpse(markdown)
            markdown = Formatter.unify_moongrum(markdown)
            markdown = Formatter.unify_rat(markdown)
            markdown = Formatter.unify_monstrous_crow(markdown)
            markdown = Formatter.unify_monstrous_dog(markdown)
            markdown = Formatter.unify_wolf(markdown)
            markdown = Formatter.unify_kindred(markdown)
            markdown = Formatter.unify_miranda_sprout(markdown)
            markdown = Formatter.unify_giant_miranda_sprout(markdown)

            markdown = Formatter.unify_swamp_of_aeonia(markdown)
            markdown = Formatter.unify_war_dead_catacombs(markdown)
            markdown = Formatter.unify_mausoleums(markdown)
            markdown = Formatter.unify_stargazers_ruins(markdown)
            markdown = Formatter.unify_elphael(markdown)
            markdown = Formatter.unify_leyndell(markdown)
            markdown = Formatter.unify_ordina(markdown)
            markdown = Formatter.unify_gelmir(markdown)
            markdown = Formatter.unify_raya_lucaria(markdown)
            markdown = Formatter.unify_liurnia(markdown)
            markdown = Formatter.unify_sellia(markdown)
            markdown = Formatter.unify_shaded_castle(markdown)

            markdown = Formatter.unify_sword_of_st_trina(markdown)
            markdown = Formatter.unify_flame_grant_me_strength(markdown)
            
            markdown = Formatter.unify_d(markdown)
            markdown = Formatter.unify_enia(markdown)
            markdown = Formatter.unify_ensha(markdown)
            markdown = Formatter.unify_ranni(markdown)
            markdown = Formatter.unify_gideon_boss(markdown)
            markdown = Formatter.unify_hewg(markdown)
            markdown = Formatter.unify_hoslow(markdown)
            markdown = Formatter.unify_iji(markdown)
            markdown = Formatter.unify_godfrey(markdown)
            markdown = Formatter.unify_gurranq(markdown)
            markdown = Formatter.unify_malenia(markdown)
            markdown = Formatter.unify_miriel(markdown)
            markdown = Formatter.unify_morgott(markdown)
            markdown = Formatter.unify_seluvis(markdown)
            markdown = Formatter.unify_varre(markdown)
            markdown = Formatter.unify_renalla(markdown)
            markdown = Formatter.unify_torrent(markdown)
            markdown = Formatter.unify_bernahl(markdown)
            markdown = Formatter.unify_nomadic_merchant_west_liurnia(markdown)
            markdown = Formatter.unify_hermit_merchant_mountaintops_east(markdown)

            markdown = Formatter.unify_skills(markdown)

            # Convert custom text markers (%%) to Markdown
            markdown = Formatter.reformat_notes(markdown)
            markdown = Formatter.reify_bullets(markdown)
            # markdown = Formatter.reify_varre_e(markdown)

            if self.category not in [Category.ARMOR]:
                markdown = Formatter.remove_notes_after_sell_value(markdown)

            if self.category in [Category.NPCS]:
                markdown = Formatter.clean_dialogue(markdown)

            if self.category in [Category.ENEMIES]:
                pass
            
            # Fix-ups
            markdown = Formatter.remove_category_links_table(markdown)
            markdown = Formatter.fix_drop_links_inside_tables(markdown)
            markdown = Formatter.add_headers_to_tables(markdown)
            markdown = Formatter.remove_elden_ring_links(markdown)
            markdown = Formatter.remove_remaining_links(markdown)

            markdown = Formatter.fix_accented_e(markdown)
            markdown = Formatter.final_whitespace_cleanup(markdown)

            # Targeted corrections
            markdown = Formatter.perform_targeted_corrections(self.name, markdown)
            markdown = Formatter.condense_newlines(markdown)
            markdown = Formatter.final_whitespace_cleanup(markdown)

            self.__dict__[name] = markdown
        else:
            self.__dict__[name] = value

    def fromMd(filename):
        #TODO
        return

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
        if self.category is not None:
            path += self.category.value + '/'

        # Create destination directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)
        
        tags_md_string = ''

        # Front matter formatting--works, but ugly!
        # if additional_tags == []:
        #     additional_tags = ''
        # else:
        #     additional_tags = '\n- ' + '\n- '.join(additional_tags)
        # tags_md_string = f'---\ntags:\n- {self.category.value}{additional_tags}\n---\n\n'
        # if self.category is not None:
        #     category_string = re.sub(r' +', r'', self.category.value)
        #     self.tags.insert(0, category_string)

        tags = ['#'+tag for tag in self.tags]

        tags_md_string = ' '.join(tags) + f'\n\n'

        if self.image is not None:
            image = '![['+self.image.name+']]\n\n'

        if self.content != '':
            content_md_string = f'{self.content}'

        output_str = tags_md_string + image + content_md_string
        
        f = open(path + filename+'.md', 'w')
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
