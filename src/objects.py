import os
import re
from enum import Enum


from constants import *


classes = [
    'Hero', 
    'Bandit', 
    'Astrologer', 
    'Warrior', 
    'Prisoner', 
    'Confessor', 
    'Wretch', 
    'Vagabond', 
    'Prophet', 
    'Samurai', 
    # Network Test classes
    'Champion', 
    'Bloody Wolf', 
    'Enchanted Knight', 
]

stats = [
    'Stats', 
    'Vigor', 
    'Vitality', 
    'Mind', 
    'Endurance', 
    'Strength', 
    'Dexterity', 
    'Intelligence', 
    'Faith', 
    'Arcane', 
    'Discovery', 
    'Affinities', 
    'Focus', 
    'HP', 
    'FP', 
    'PvP', 
    'Poise', 
    'Robustness', 
    'Stamina', 
    'Immunity', 
    'Hardness', 
    'Equip Load', 
    'Fall Damage', 
    'Physical Damage', 
    'Standard Damage', 
    'Strike Damage', 
    'Pierce Damage', 
    'Slash Damage', 
    'Critical Damage', 
    'Magic Damage', 
    'Lightning Damage', 
    'Holy Damage', 
    'Fire Damage', 
    'Fire Damage Negation', 
    'Magic Damage Negation', 
    'Physical Defense', 
    'Standard Defense', 
    'Strike Defense', 
    'Pierce Defense', 
    'Slash Defense', 
    'Critical Defense', 
    'Magic Defense', 
    'Lightning Defense', 
    'Holy Defense', 
    'Fire Defense', 
    'damage types', 
    'Dodging', 
    'Guarding', 
    'Arrows and Bolts' # Subsection of Items
]

status_effects = [
    'Status Effects', 
    'Buffs and Debuffs', 
    'Poison', 
    'Scarlet Rot', 
    'Blood Loss', 
    'Bleed', 
    'Frostbite', 
    'Sleep', 
    'Madness', 
    'Death Blight', 
    'Instant Death', 
    'Hemorrhage', 
    '/Hemorrhage', 
]

items_to_hide = [
    'Ghost Glovewort (1)', 
    'Ghost Glovewort (2)', 
    'Ghost Glovewort (3)', 
    'Ghost Glovewort (4)', 
    'Ghost Glovewort (5)', 
    'Ghost Glovewort (6)', 
    'Ghost Glovewort (7)', 
    'Ghost Glovewort (8)', 
    'Ghost Glovewort (9)', 
    'Grave Glovewort (1)', 
    'Grave Glovewort (2)', 
    'Grave Glovewort (3)', 
    'Grave Glovewort (4)', 
    'Grave Glovewort (5)', 
    'Grave Glovewort (6)', 
    'Grave Glovewort (7)', 
    'Grave Glovewort (8)', 
    'Grave Glovewort (9)', 
    'Smithing Stone (1)', 
    'Smithing Stone (2)', 
    'Smithing Stone (3)', 
    'Smithing Stone (4)', 
    'Smithing Stone (5)', 
    'Smithing Stone (6)', 
    'Smithing Stone (7)', 
    'Smithing Stone (8)', 
    'Somber Smithing Stone (1)', 
    'Somber Smithing Stone (2)', 
    'Somber Smithing Stone (3)', 
    'Somber Smithing Stone (4)', 
    'Somber Smithing Stone (5)', 
    'Somber Smithing Stone (6)', 
    'Somber Smithing Stone (7)', 
    'Somber Smithing Stone (8)', 
    'Somber Smithing Stone (9)', 
]

spell_type = [
    'Sorceries', 
    'Sorcery', 
    'Bestial Incantations', 
    'Blood Incantations', 
    'Dragon Communion Incantations', 
    'Dragon Cult Incantations', 
    'Erdtree Incantations', 
    'Fire Giant Incantations', 
    'Fire Monk Incantations', 
    'Frenzied Flame Incantations', 
    'Godskin Apostle Incantations', 
    'Godslayer Incantations', 
    'Golden Order Incantations', 
    'Servants of Rot Incantations', 
    'Two Fingers Incantations', 
    "Two Fingers' Incantations", 
    #------------------------------
    'Incantations', 
    'Aberrant Sorceries', 
    'Carian Sorceries', 
    'Claymen Sorceries', 
    'Crystalian Sorceries', 
    'Death Sorceries', 
    'Full Moon Sorceries', 
    'Glintstone Sorceries', 
    'Gravity Sorceries', 
    "Loretta's Sorceries", 
    'Magma Sorceries', 
    'Night Sorceries', 
    'Primeval Sorceries', 
    'Cold Sorceries', 
]

armor_type = [
    'Armor', 
    'Gauntlets', 
    'Helms', 
    'Chest Armor', 
    'Leg Armor', 
]

weapon_type = [
    'Weapons', 
    'Daggers', 
    'Straight Swords', 
    'Greatswords', 
    'Colossal Swords ', 
    'Thrusting Swords', 
    'Heavy Thrusting Swords', 
    'Curved Swords', 
    'Curved Greatswords', 
    'Katanas', 
    'Twinblades', 
    'Axes', 
    'Greataxes', 
    'Hammers', 
    'Flails', 
    'Great Hammers', 
    'Colossal Weapons', 
    'Spears', 
    'Great Spears', 
    'Halberds', 
    'Reapers', 
    'Whips', 
    'Fists', 
    'Claws', 
    'Light Bows', 
    'Bows', 
    'Greatbows', 
    'Crossbows', 
    'Ballistae', 
    'Glintstone Staffs', 
    'Sacred Seals', 
    'Torches', 
    'Tools', 
]

shield_type = [
    'Small Shields', 
    'Medium Shields', 
    'Greatshields', 
]

sites_of_grace = [
    'Saintsbridge', 
]

hide_list = [
    'Classes', 
    'Ashes of War', 
    'Consumables', 
    'Magic', 
    'Magic Spells', 
    'Spells', 
    'Runes', 
    'Skills', 
    'Bell Bearings', 
    'Keepsakes', 
    'Smithing Stones', 
    'Somber Smithing Stones', 
    'Patch Notes', 
    'Creatures and Enemies', 
    'New Game Plus', 
    'Upgrades', 
    'Upgrade Materials', 
    'Materials', 
    'Crafting', 
    'Crafting Materials', 
    'Cookbooks', 
    'Builds', 
    'Parry', 
    'Parrying', 
    'Sites of Grace', 
    'Site of Grace', 
    'Skeletons', 
    'Stance', 
    'Rebirth', 
    'NPC Summons', 
    'NPC Invaders', 
    'Spirit Ashes', 
    'Legendary Spirit Ashes', 
    'Gestures', 
    'Bosses', 
    'Lore', 
    'NPCs', 
    'Great Runes', 
    'Smithing Stone', 
    'Stakes of Marika', 
    'Remembrance', 
    'Remembrance Weapons (Boss Weapons)', 
    'Network Test and Demo', 
    'Elden Ring Closed Network Test', 
    'Wiki', 
    'Player Trade', 
    'Endings', 
    'Talismans', 
    'Side Quests', 
    'Illusory Walls', 
    'Memory Slots', 
    'Mausoleum Compound', 
    'Waygates', 
    'Multiplayer Coop and Online', 
    'Crystal Tears', 
    'Character Creation', 
    'Ghost Gloveworts', 
    'Golden Runes', 
    'Shields', 
    'Spiritspring', 
    'Ballistas', 
    'Foot Soldier', 
    'Locations', 
    'Merchants', 
    'Nomadic Merchants', 
    'Divine Towers', 
    'Erdtree', 
    'Outer Gods', 
    'Paintings', 
    'Multiplayer Items', 
    'Legendary Armaments',  #TODO: Tag Legendary Armaments, change links to bring up tagged pages
]

class Category(Enum):
    NONE = 'None'
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
    'Ranni the Witch':                          'Ranni', 
    'Torrent (Spirit Steed)':                   'Torrent', 
    'Preceptor Seluvis':                        'Seluvis', 
    'Gurranq Beast Clergyman':                  'Gurranq, Beast Clergyman', 
    'Morgott the Omen King':                    'Morgott, the Omen King', 
    'Moongrum Carian Knight':                   'Moongrum, Carian Knight', 
    'Iron Fist Alexander':                      'Alexander', 
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
