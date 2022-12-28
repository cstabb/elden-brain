import configparser
from pathlib import Path

CONFIG_FILENAME = 'config.ini'
class ConfigWriter:
    
    def writeOption(section, option, value):
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        path = Path(__file__).parent / CONFIG_FILENAME
        read_result = config.read(path)

        config[section][option] = value

        with open(path, 'w') as configfile:    # save
            config.write(configfile)

class ConfigReader:

    def toBool(self, text):
        if text in ['True', 'true']:
            return True
        elif text in ['False', 'false']:
            return False
        else:
            raise TypeError('Config parse error, boolean options must be True or False')

    def __init__(self):
        ## Set up config
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str
        path = Path(__file__).parent / CONFIG_FILENAME
        read_result = self.config.read(path)

        # Assign options from config
        self.wiki_url = self.config['Main']['wiki_url']
        if self.wiki_url == '':
            raise ValueError('The wiki URL has not been set, update config.ini with the appropriate value')
        self.cache_location = self.config['Local Directories']['cache_location'] + '/'
        self.vault_name = self.config['Local Directories']['vault_name'] + '/'

        self.item_subcategory_folders = self.config['Options']['item_subcategory_folders']

        # Remapping the remapping
        self.remap_assets = self.toBool(self.config['Remapping']['remap_assets'])
        self.remap_assets_to = self.config['Remapping']['remap_assets_to']
        self.remap_bosses = self.toBool(self.config['Remapping']['remap_bosses'])
        self.remap_bosses_to = self.config['Remapping']['remap_bosses_to']
        self.remap_creatures_and_enemies = self.toBool(self.config['Remapping']['remap_creatures_and_enemies'])
        self.remap_creatures_and_enemies_to = self.config['Remapping']['remap_creatures_and_enemies_to']
        self.remap_hidden = self.toBool(self.config['Remapping']['remap_hidden'])
        self.remap_hidden_to = self.config['Remapping']['remap_hidden_to']
        self.remap_items = self.toBool(self.config['Remapping']['remap_items'])
        self.remap_items_to = self.config['Remapping']['remap_items_to']
        self.remap_legacy_dungeons = self.toBool(self.config['Remapping']['remap_legacy_dungeons'])
        self.remap_legacy_dungeons_to = self.config['Remapping']['remap_legacy_dungeons_to']
        self.remap_locations = self.toBool(self.config['Remapping']['remap_locations'])
        self.remap_locations_to = self.config['Remapping']['remap_locations_to']
        self.remap_lore = self.toBool(self.config['Remapping']['remap_lore'])
        self.remap_lore_to = self.config['Remapping']['remap_lore_to']
        self.remap_merchants = self.toBool(self.config['Remapping']['remap_merchants'])
        self.remap_merchants_to = self.config['Remapping']['remap_merchants_to']
        self.remap_npcs = self.toBool(self.config['Remapping']['remap_npcs'])
        self.remap_npcs_to = self.config['Remapping']['remap_npcs_to']
        self.remap_shields = self.toBool(self.config['Remapping']['remap_shields'])
        self.remap_shields_to = self.config['Remapping']['remap_shields_to']
        self.remap_skills = self.toBool(self.config['Remapping']['remap_skills'])
        self.remap_skills_to = self.config['Remapping']['remap_skills_to']
        self.remap_spells = self.toBool(self.config['Remapping']['remap_spells'])
        self.remap_spells_to = self.config['Remapping']['remap_spells_to']
        self.remap_talismans = self.toBool(self.config['Remapping']['remap_talismans'])
        self.remap_talismans_to = self.config['Remapping']['remap_talismans_to']
        self.remap_weapons = self.toBool(self.config['Remapping']['remap_weapons'])
        self.remap_weapons_to = self.config['Remapping']['remap_weapons_to']
        self.remap_armor = self.toBool(self.config['Remapping']['remap_armor'])
        self.remap_armor_to = self.config['Remapping']['remap_armor_to']
        self.remap_spirit_ashes = self.toBool(self.config['Remapping']['remap_spirit_ashes'])
        self.remap_spirit_ashes_to = self.config['Remapping']['remap_spirit_ashes_to']
        # Armor sub-categories
        self.remap_chest_armor = self.toBool(self.config['Remapping']['remap_chest_armor'])
        self.remap_chest_armor_to = self.config['Remapping']['remap_chest_armor_to']
        self.remap_gauntlets = self.toBool(self.config['Remapping']['remap_gauntlets'])
        self.remap_gauntlets_to = self.config['Remapping']['remap_gauntlets_to']
        self.remap_helms = self.toBool(self.config['Remapping']['remap_helms'])
        self.remap_helms_to = self.config['Remapping']['remap_helms_to']
        self.remap_leg_armor = self.toBool(self.config['Remapping']['remap_leg_armor'])
        self.remap_leg_armor_to = self.config['Remapping']['remap_leg_armor_to']
        # Item sub-categories
        self.remap_key_items = self.toBool(self.config['Remapping']['remap_key_items'])
        self.remap_key_items_to = self.config['Remapping']['remap_key_items_to']
        self.remap_arrows_and_bolts = self.toBool(self.config['Remapping']['remap_arrows_and_bolts'])
        self.remap_arrows_and_bolts_to = self.config['Remapping']['remap_arrows_and_bolts_to']
        self.remap_bell_bearings = self.toBool(self.config['Remapping']['remap_bell_bearings'])
        self.remap_bell_bearings_to = self.config['Remapping']['remap_bell_bearings_to']
        self.remap_cookbooks = self.toBool(self.config['Remapping']['remap_cookbooks'])
        self.remap_cookbooks_to = self.config['Remapping']['remap_cookbooks_to']
        self.remap_consumables = self.toBool(self.config['Remapping']['remap_consumables'])
        self.remap_consumables_to = self.config['Remapping']['remap_consumables_to']
        self.remap_materials = self.toBool(self.config['Remapping']['remap_materials'])
        self.remap_materials_to = self.config['Remapping']['remap_materials_to']
        self.remap_crystal_tears = self.toBool(self.config['Remapping']['remap_crystal_tears'])
        self.remap_crystal_tears_to = self.config['Remapping']['remap_crystal_tears_to']
        self.remap_great_runes = self.toBool(self.config['Remapping']['remap_great_runes'])
        self.remap_great_runes_to = self.config['Remapping']['remap_great_runes_to']
        self.remap_info_items = self.toBool(self.config['Remapping']['remap_info_items'])
        self.remap_info_items_to = self.config['Remapping']['remap_info_items_to']
        self.remap_multiplayer_items = self.toBool(self.config['Remapping']['remap_multiplayer_items'])
        self.remap_multiplayer_items_to = self.config['Remapping']['remap_multiplayer_items_to']
        self.remap_remembrance = self.toBool(self.config['Remapping']['remap_remembrance'])
        self.remap_remembrance_to = self.config['Remapping']['remap_remembrance_to']
        self.remap_tools = self.toBool(self.config['Remapping']['remap_tools'])
        self.remap_tools_to = self.config['Remapping']['remap_tools_to']
        self.remap_whetblades = self.toBool(self.config['Remapping']['remap_whetblades'])
        self.remap_whetblades_to = self.config['Remapping']['remap_whetblades_to']
        self.remap_upgrade_materials = self.toBool(self.config['Remapping']['remap_upgrade_materials'])
        self.remap_upgrade_materials_to = self.config['Remapping']['remap_upgrade_materials_to']

        # Data
        self.legacy_dungeons = self.parseList(self.config['Data']['legacy_dungeons'])
        self.legacy_dungeons.sort()

        # Hidden
        self.hidden = self.config['Hidden']
        
    def parseList(self, text):
        return text.split('\n')[1:]