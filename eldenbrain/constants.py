from .config import ConfigReader

cfg = ConfigReader()

def urlify(name=''):
    return name.replace(' ', '+')

### The wiki URL
WIKI_URL = cfg.wiki_url

### Local directories
LOCAL_CACHE = cfg.cache_location
LOCAL_VAULT_NAME = cfg.vault_name
LOCAL_ASSETS = (cfg.remap_assets_to if cfg.remap_assets else 'Assets') + '/'    # If this is set, also set Obsidian's Attachment folder path to the same value (found in Settings->Files & Links)
LOCAL_HIDDEN = (cfg.remap_hidden_to if cfg.remap_hidden else 'Hidden') + '/'

### Paths (relative to the wiki url)
## Category paths
PATH_WEAPONS                = WIKI_URL + '/' + cfg.remap_weapons_to
PATH_SPIRIT_ASHES           = WIKI_URL + '/' + cfg.remap_spirit_ashes_to
PATH_SKILLS                 = WIKI_URL + '/' + cfg.remap_skills_to
PATH_SPELLS                 = WIKI_URL + '/' + cfg.remap_spells_to
PATH_SHIELDS                = WIKI_URL + '/' + cfg.remap_shields_to
PATH_ARMOR                  = WIKI_URL + '/' + cfg.remap_armor_to
PATH_ARMOR_HELMS            = WIKI_URL + '/' + cfg.remap_helms_to
PATH_ARMOR_CHESTS           = WIKI_URL + '/' + cfg.remap_chest_armor_to
PATH_ARMOR_GAUNTLETS        = WIKI_URL + '/' + cfg.remap_gauntlets_to
PATH_ARMOR_LEGS             = WIKI_URL + '/' + cfg.remap_leg_armor_to
PATH_TALISMANS              = WIKI_URL + '/' + cfg.remap_talismans_to
PATH_CREATURES_AND_ENEMIES  = WIKI_URL + '/' + cfg.remap_creatures_and_enemies_to
PATH_BOSSES                 = WIKI_URL + '/' + cfg.remap_bosses_to
PATH_LEGACY_DUNGEONS        = WIKI_URL + '/' + cfg.remap_legacy_dungeons_to
PATH_LOCATIONS              = WIKI_URL + '/' + cfg.remap_locations_to
PATH_NPCS                   = WIKI_URL + '/' + cfg.remap_npcs_to
PATH_MERCHANTS              = WIKI_URL + '/' + cfg.remap_merchants_to
PATH_LORE                   = WIKI_URL + '/' + cfg.remap_lore_to   # Used for scraping transcripts
PATH_ITEMS                  = WIKI_URL + '/' + cfg.remap_items_to  # Not used--item index pages are listed below

## Item sub-category paths
PATH_KEY_ITEMS              = WIKI_URL + '/' + urlify(cfg.remap_key_items_to)
PATH_ARROWS_AND_BOLTS       = WIKI_URL + '/' + cfg.remap_arrows_and_bolts_to
PATH_BELL_BEARINGS          = WIKI_URL + '/' + cfg.remap_bell_bearings_to
PATH_COOKBOOKS              = WIKI_URL + '/' + cfg.remap_cookbooks_to
PATH_CONSUMABLES            = WIKI_URL + '/' + cfg.remap_consumables_to
PATH_CRAFTING_MATERIALS     = WIKI_URL + '/' + cfg.remap_materials_to
PATH_CRYSTAL_TEARS          = WIKI_URL + '/' + cfg.remap_crystal_tears_to
PATH_GREAT_RUNES            = WIKI_URL + '/' + cfg.remap_great_runes_to
PATH_INFO_ITEMS             = WIKI_URL + '/' + cfg.remap_info_items_to
PATH_MULTIPLAYER_ITEMS      = WIKI_URL + '/' + cfg.remap_multiplayer_items_to
PATH_REMEMBRANCE            = WIKI_URL + '/' + cfg.remap_remembrance_to
PATH_TOOLS                  = WIKI_URL + '/' + cfg.remap_tools_to
PATH_WHETBLADES             = WIKI_URL + '/' + cfg.remap_whetblades_to
PATH_UPGRADE_MATERIALS      = WIKI_URL + '/' + cfg.remap_upgrade_materials_to

## Stretch Goals
PATH_EFFIGIES_OF_THE_MARTYR = WIKI_URL + '/Effigies of the Martyr'
PATH_SITES_OF_GRACE         = WIKI_URL + '/Sites of Grace'

## Tags
# Note: Most tags are derived
HIDDEN_TAG = '#Hidden'

## Data
LEGACY_DUNGEONS_LIST = [#cfg.legacy_dungeons
    'Crumbling Farum Azula', 
    'Elphael, Brace of the Haligtree', 
    'Leyndell Royal Capital (Legacy Dungeon)', # "Leyndell, Royal Capital (Legacy Dungeon)" leads to a 404, page needs to be renamed at the wiki level
    "Miquella's Haligtree",
    'Raya Lucaria Academy', 
    'Stormveil Castle', 
    'Volcano Manor', 
]
HIDDEN_LIST = cfg.hidden