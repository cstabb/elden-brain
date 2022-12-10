import os
import re
from enum import Enum

from markdownify import markdownify as md

from constants import *
from text_handling import Formatter

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

unobtainable = [
    "Millicent's Set", 
    'Ragged Set', 
    "Brave's Set", 
    'Deathbed Set', 
    'Deathbed Smalls', 
    'Grass Hair Ornament', 
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
            self.add_tag('Hidden')
        
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

            # Pre-Markdownify modifications
            # text = Formatter.prep_varre_e(text)

            # Markdownify
            markdown = md(text)

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
            # markdown = Formatter.unlink_sites_of_grace(markdown)
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

            # Convert custom text markers to Markdown
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

    def from_md(filename):
        #TODO
        return

    def add_tag(self, tag):
        tag = re.sub(r' +', r'', tag)
        if tag not in self.tags:
            self.tags.append(tag)

    # def derive_path(self):
    #     self.path = '/' + self.name.replace(' ', '+')

    def set_location(self, location_in_html):
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
        
        f = open(path + filename+'.md', 'w')
        
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
        #     # print(tags)
        tags = ['#'+tag for tag in self.tags]
        # print(tags)
        tags_md_string = ' '.join(tags) + f'\n\n'

        image = ''
        if self.image is not None:
            image = '![['+self.image.name+']]\n\n'

        content_md_string = ''
        if self.content != '':
            content_md_string = f'{self.content}'

        output_str = tags_md_string + image + content_md_string
        # print(output_str)
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
