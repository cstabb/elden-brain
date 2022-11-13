import logging
import os
import time
from enum import Enum

from constants import *
from scraper import Scraper

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

class EldenBring:
    """
    """

    classes = [
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
        "FP", 
        "Poise", 
        "Robustness", 
        "Standard Damage", 
        "Strike Damage", 
        "Critical Damage", 
    ]

    status_effects = [
        "Poison", 
        "Scarlet Rot", 
        "Blood Loss", 
        "Frostbite", 
        "Sleep", 
        "Madness", 
        "Death Blight", 
        "Hemorrhage", 
        "/Hemorrhage", 
    ]

    spell_type = [
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

    weapon_type = [
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
        "Smithing Stones", 
        "Somber Smithing Stones", 
        "Patch Notes", 
        "Creatures and Enemies", 
        "New Game Plus", 
        "Upgrades", 
        "Crafting Materials", 
        "Cookbooks", 
    ]

    def __init__(self, logging_enabled=True):
        # Create directories if they don't already exist
        if not os.path.exists(LOCAL_CACHE):
            os.mkdir(LOCAL_CACHE)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS)
        if not os.path.exists(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN):
            os.mkdir(LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN)

        # Set up logger
        if logging_enabled:
            logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
            self.log = logging.getLogger('elden-bring-logger')
        else:
            self.log = logging.getLogger('null_logger').addHandler(logging.NullHandler())

        self.scraper = Scraper(self.log)

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
        all_targets = self.classes + self.stats + self.status_effects + \
                      self.weapon_type + self.shield_type + self.hide_list
        destination_path = LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_HIDDEN

        self.log.info(f"Creating {len(all_targets)} hidden files...")

        for idx, target in enumerate(all_targets):
            # Create a new file if it doesn't exist or overwrite is True
            if overwrite or not os.path.isfile(destination_path + target):
                self.log.info(f"Writing {target} hidden file [{idx+1} of {len(all_targets)}]...")
                f = open(destination_path + target + '.md', 'w')
                f.write(HIDDEN_TAG)
                f.close()
                time.sleep(0.001)   # Necessary to allow Obsidian time to update with the new file

    def create_weapons(self, overwrite=True):
        """
        """
        urls = self.scraper.get_weapons_urls()
        entities = self.scraper.convert_urls_to_entities(urls)

        for idx, entity in enumerate(entities):
            self.log.info(f"Writing {entity.name} [{idx+1} of {len(entities)}]...")
            entity.write()
            #time.sleep(0.001)

    def create_shields(self, overwrite=True):
        """
        """
        urls = self.scraper.get_shields_urls()
        entities = self.scraper.convert_urls_to_entities(urls)

        self.log.info(f"Parsing {len(entities)} Shields...")
        
        for idx, entity in enumerate(entities):
            self.log.info(f"Writing {entity.name} [{idx+1} of {len(entities)}]...")
            entity.write()

    def create_armor(self, overwrite=True):
        #TODO
        pass

    def create_items(self, overwrite=True):
        """
        """
        urls = self.scraper.get_items_urls()
        self.scraper.convert_urls_to_entities(urls, EntityType.ITEM)

    def create_locations(self, overwrite=True):
        """
        """
        urls = self.scraper.get_locations_urls()
        self.scraper.convert_urls_to_entities(urls, EntityType.LOCATION)

    def create_legacy_dungeons(self, overwrite=True):
        """
        """
        urls = self.scraper.get_legacy_dungeons_urls()
        self.scraper.convert_urls_to_entities(urls, EntityType.LOCATION)

    def create_spells(self, overwrite=True):
        """
        """
        urls = self.scraper.get_spells_urls()
        self.scraper.convert_urls_to_entities(urls, EntityType.SPELL)

    def create_spirit_ashes(self, overwrite=True):
        #TODO
        pass

    def create_creatures_and_enemies(self, overwrite=True):
        """
        """
        urls = self.scraper.get_creatures_and_enemies_urls()
        self.scraper.convert_urls_to_entities(urls, EntityType.ENEMY)

    def create_bosses(self, overwrite=True):
        """
        """
        urls = self.scraper.get_bosses_urls()
        # print(urls)
        # print(len(urls))
        self.scraper.convert_urls_to_entities(urls, EntityType.BOSS)

    def create_npcs(self, overwrite=True):
        """
        """
        urls = self.scraper.get_npcs_urls()
        self.scraper.convert_urls_to_entities(urls, EntityType.NPC)