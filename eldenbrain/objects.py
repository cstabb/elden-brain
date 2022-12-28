import os
import re
from enum import Enum

from .constants import *


class Category(Enum):
    ARMOR = 'Armor'
    BOSSES = 'Bosses'
    ENEMIES = 'Creatures and Enemies'
    HIDDEN = 'Hidden'
    ITEMS = 'Items'
    LEGACY_DUNGEONS = 'Legacy Dungeons'
    LOCATIONS = 'Locations'
    NPCS = 'NPCs'
    SHIELDS = 'Shields'
    SKILLS = 'Skills'
    SPELLS = 'Spells'
    SPIRIT_ASH = 'Spirit Ashes'
    TALISMANS = 'Talismans'
    WEAPONS = 'Weapons'

category_paths = {
    Category.ARMOR: PATH_ARMOR, 
    Category.BOSSES: PATH_BOSSES,
    Category.ENEMIES: PATH_CREATURES_AND_ENEMIES,
    Category.ITEMS: PATH_ITEMS,
    Category.LEGACY_DUNGEONS: PATH_LEGACY_DUNGEONS,
    Category.LOCATIONS: PATH_LOCATIONS,
    Category.NPCS: PATH_NPCS,
    Category.SHIELDS: PATH_SHIELDS,
    Category.SKILLS: PATH_SKILLS,
    Category.SPELLS: PATH_SPELLS,
    Category.SPIRIT_ASH: PATH_SPIRIT_ASHES, 
    Category.TALISMANS: PATH_TALISMANS, 
}

class ArmorSubcategory(Enum):
    ARMOR_SET = 'Armor Sets'
    CHEST = 'Chest Armor'
    GAUNTLET = 'Gauntlets'
    HELM = 'Helms'
    LEG = 'Leg Armor'

armor_subcategory_paths = {
    ArmorSubcategory.CHEST: PATH_ARMOR_CHESTS, 
    ArmorSubcategory.GAUNTLET: PATH_ARMOR_GAUNTLETS, 
    ArmorSubcategory.HELM: PATH_ARMOR_HELMS, 
    ArmorSubcategory.LEG: PATH_ARMOR_LEGS, 
}

class ItemSubcategory(Enum):
    ARROWS_AND_BOLTS = 'Arrows and Bolts'
    BELL_BEARINGS = 'Bell Bearings'
    CONSUMABLES = 'Consumables'
    COOKBOOKS = 'Cookbooks'
    CRAFTING_MATERIALS = 'Crafting Materials'
    CRYSTAL_TEARS = 'Crystal Tears'
    GREAT_RUNES = 'Great Runes'
    INFO_ITEMS = 'Info Items'
    KEY_ITEMS = 'Key Items'
    MULTIPLAYER_ITEMS = 'Multiplayer Items'
    REMEMBRANCE = 'Remembrance'
    TOOLS = 'Tools'
    UPGRADE_MATERIALS = 'Upgrade Materials'
    WHETBLADES = 'Whetblades'

item_subcategory_paths = {
    ItemSubcategory.ARROWS_AND_BOLTS: PATH_ARROWS_AND_BOLTS,
    ItemSubcategory.BELL_BEARINGS: PATH_BELL_BEARINGS,
    ItemSubcategory.CONSUMABLES: PATH_CONSUMABLES,
    ItemSubcategory.COOKBOOKS: PATH_COOKBOOKS,
    ItemSubcategory.CRAFTING_MATERIALS: PATH_CRAFTING_MATERIALS,
    ItemSubcategory.CRYSTAL_TEARS: PATH_CRYSTAL_TEARS,
    ItemSubcategory.GREAT_RUNES: PATH_GREAT_RUNES,
    ItemSubcategory.INFO_ITEMS: PATH_INFO_ITEMS,
    ItemSubcategory.KEY_ITEMS: PATH_KEY_ITEMS,
    ItemSubcategory.MULTIPLAYER_ITEMS: PATH_MULTIPLAYER_ITEMS,
    ItemSubcategory.REMEMBRANCE: PATH_REMEMBRANCE,
    ItemSubcategory.TOOLS: PATH_TOOLS,
    ItemSubcategory.UPGRADE_MATERIALS: PATH_UPGRADE_MATERIALS,
    ItemSubcategory.WHETBLADES: PATH_WHETBLADES,
}

name_overrides = {
    # NPCs
    'Ranni the Witch':                          'Ranni', 
    'Torrent (Spirit Steed)':                   'Torrent', 
    'Preceptor Seluvis':                        'Seluvis', 
    'Gurranq Beast Clergyman':                  'Gurranq, Beast Clergyman', 
    'Morgott the Omen King':                    'Morgott, the Omen King', 
    'Iron Fist Alexander':                      'Alexander', 

    # Locations
    'Leyndell Royal Capital (Legacy Dungeon)':  'Leyndell, Royal Capital (Legacy Dungeon)',

    # Bosses, Creatures, Enemies
    'Moongrum Carian Knight':                   'Moongrum, Carian Knight', 
    'Giant Dog':                                'Monstrous Dog', 
    'Giant Crow':                               'Monstrous Crow',
    'Gauntlets':                                'Chain Gauntlets', 
    'Lesser Kindred of Rot (Pests)':            'Lesser Kindred of Rot', 

    # Spells
    'Flame Grant me Strength':                  'Flame, Grant Me Strength', 
    'Flame Grant Me Strength':                  'Flame, Grant Me Strength', 
    'Flame Fall Upon Them':                     'Flame, Fall Upon Them', 
    'Flame Protect Me':                         'Flame, Protect Me', 
    'Flame Cleanse Me':                         'Flame, Cleanse Me', 
    'Surge O Flame!':                           'Surge, O Flame!', 
    'Burn O Flame!':                            'Burn, O Flame!', 
    'Whirl O Flame!':                           'Whirl, O Flame!', 
    'O Flame!':                                 'O, Flame!', 

    # Skills
    'Parry Skill':                              'Parry (Skill)', 
    'Carian Greatsword Skill':                  'Carian Greatsword (Skill)', 
    'Glintstone Pebble Skill':                  'Glintstone Pebble (Skill)', 
    'Great Oracular Bubble Skill':              'Great Oracular Bubble (Skill)', 
    # 'Ash of War: No Skill':                    'No Skill', 
    # 'Unblockable Blade Skill':                  'Unblockable Blade (Skill)', 
    'Flowing Form':                             'Flowing Form (Nox Flowing Sword)', 
    # Enemies/Bosses
    'Astel Naturalborn of the Void':            'Astel, Naturalborn of the Void', 
    'Bols Carian Knight':                       'Bols, Carian Knight', 
    'Skeletons':                                'Skeleton', 
    'Walking Mausoleum':                        'Wandering Mausoleum', 
    'Cathedral of Dragon Communion (Caelid)':   'Cathedral of Dragon Communion', 
    'Rennala, Queen of the Full Moon (NPC)':    'Rennala', 
    "Kalé's Bell Bearing":                      "Kale's Bell Bearing", 
    'Wandering Merchant Caelid Highway North':  'Nomadic Merchant Caelid Highway North',
    'Wandering Merchant Ainsel River':          'Hermit Merchant Ainsel River',
    'Boc the Seamster':                         'Boc', 
    'White Mask Varré':                         'White Mask Varre', # Hate to do this, but...
}
