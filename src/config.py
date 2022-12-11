import configparser

class ConfigReader:

    def __init__(self):
        ## Set up config
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.config.read('config.ini')

        # Assign options from config
        self.wiki_url = self.config['Main']['wiki_url']
        self.cache_location = self.config['Local Directories']['cache_location'] + '/'
        self.vault_name = self.config['Local Directories']['vault_name'] + '/'

        self.item_subcategory_folders = self.config['Options']['item_subcategory_folders']

        # Remapping the remapping
        self.remap_assets = self.config['Remapping']['remap_assets']
        self.remap_assets_to = self.config['Remapping']['remap_assets_to']
        self.remap_bosses = self.config['Remapping']['remap_bosses']
        self.remap_bosses_to = self.config['Remapping']['remap_bosses_to']
        self.remap_creatures_and_enemies = self.config['Remapping']['remap_creatures_and_enemies']
        self.remap_creatures_and_enemies_to = self.config['Remapping']['remap_creatures_and_enemies_to']
        self.remap_hidden = self.config['Remapping']['remap_hidden']
        self.remap_hidden_to = self.config['Remapping']['remap_hidden_to']
        self.remap_items = self.config['Remapping']['remap_items']
        self.remap_items_to = self.config['Remapping']['remap_items_to']
        self.remap_legacy_dungeons = self.config['Remapping']['remap_legacy_dungeons']
        self.remap_legacy_dungeons_to = self.config['Remapping']['remap_legacy_dungeons_to']
        self.remap_locations = self.config['Remapping']['remap_locations']
        self.remap_locations_to = self.config['Remapping']['remap_locations_to']
        self.remap_lore = self.config['Remapping']['remap_lore']
        self.remap_lore_to = self.config['Remapping']['remap_lore_to']
        self.remap_merchants = self.config['Remapping']['remap_merchants']
        self.remap_merchants_to = self.config['Remapping']['remap_merchants_to']
        self.remap_npcs = self.config['Remapping']['remap_npcs']
        self.remap_npcs_to = self.config['Remapping']['remap_npcs_to']
        self.remap_shields = self.config['Remapping']['remap_shields']
        self.remap_shields_to = self.config['Remapping']['remap_shields_to']
        self.remap_skills = self.config['Remapping']['remap_skills']
        self.remap_skills_to = self.config['Remapping']['remap_skills_to']
        self.remap_spells = self.config['Remapping']['remap_spells']
        self.remap_spells_to = self.config['Remapping']['remap_spells_to']
        self.remap_talismans = self.config['Remapping']['remap_talismans']
        self.remap_talismans_to = self.config['Remapping']['remap_talismans_to']
        self.remap_weapons = self.config['Remapping']['remap_weapons']
        self.remap_weapons_to = self.config['Remapping']['remap_weapons_to']
        self.remap_armor = self.config['Remapping']['remap_armor']
        self.remap_armor_to = self.config['Remapping']['remap_armor_to']
        self.remap_spirit_ashes = self.config['Remapping']['remap_spirit_ashes']
        self.remap_spirit_ashes_to = self.config['Remapping']['remap_spirit_ashes_to']
        # Armor sub-categories
        self.remap_chest_armor = self.config['Remapping']['remap_chest_armor']
        self.remap_chest_armor_to = self.config['Remapping']['remap_chest_armor_to']
        self.remap_gauntlets = self.config['Remapping']['remap_gauntlets']
        self.remap_gauntlets_to = self.config['Remapping']['remap_gauntlets_to']
        self.remap_helms = self.config['Remapping']['remap_helms']
        self.remap_helms_to = self.config['Remapping']['remap_helms_to']
        self.remap_leg_armor = self.config['Remapping']['remap_leg_armor']
        self.remap_leg_armor_to = self.config['Remapping']['remap_leg_armor_to']
        # Item sub-categories
        self.remap_key_items_to = self.config['Remapping']['remap_key_items_to']
        self.remap_arrows_and_bolts_to = self.config['Remapping']['remap_arrows_and_bolts_to']
        self.remap_bell_bearings_to = self.config['Remapping']['remap_bell_bearings_to']
        self.remap_cookbooks_to = self.config['Remapping']['remap_cookbooks_to']
        self.remap_consumables_to = self.config['Remapping']['remap_consumables_to']
        self.remap_materials_to = self.config['Remapping']['remap_materials_to']
        self.remap_crystal_tears_to = self.config['Remapping']['remap_crystal_tears_to']
        self.remap_great_runes_to = self.config['Remapping']['remap_great_runes_to']
        self.remap_info_items_to = self.config['Remapping']['remap_info_items_to']
        self.remap_multiplayer_items_to = self.config['Remapping']['remap_multiplayer_items_to']
        self.remap_remembrance_to = self.config['Remapping']['remap_remembrance_to']
        self.remap_tools_to = self.config['Remapping']['remap_tools_to']
        self.remap_whetblades_to = self.config['Remapping']['remap_whetblades_to']
        self.remap_upgrade_materials_to = self.config['Remapping']['remap_upgrade_materials_to']

        # Data
        self.legacy_dungeons = self.parseList(self.config['Data']['legacy_dungeons'])

        # Hidden
        self.hidden = self.config['Hidden']
        
    def parseList(self, text):
        return text.split('\n')[1:]