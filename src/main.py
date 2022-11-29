from elden_bring import *
from scraper import Scraper

from objects import *

def main():

    eb = EldenBring()

    # Refactor 2.0 workflow
    # eb.list_categories()
    # eb.update_entity_names(Category.BOSSES)
    # print(eb.get_entity_names(Category.WEAPONS))
    # hidden_entities_names = eb.get_entity_names(Category.HIDDEN)
    # hidden_entities = eb.create_entities(hidden_entities_names) # Create shells without content
    # eb.add_tag(hidden_entities, "NewTag")
    # hidden_entities = [entity for entity in entities where entity.name not in drop_list]
    # hidden_entities = eb.scrape_entities(hidden_entities_names, write=False) # Default
    # hidden_entities = eb.scrape_entities(hidden_entities_names, write=True, directory="/Hidden") # If entities have already been scraped, don't rescrape
    # eb.write_entities(hidden_entities, directory="/Hidden") # Redundant if the above has been run; will rewrite over files just created
    
    # eb.create_hidden()

    # eb.scrape_entities(Category.WEAPONS, write=True)
    # eb.scrape_entities(Category.SHIELDS, write=True)
    # eb.scrape_entities(Category.ARMOR, write=True)
    # eb.scrape_entities(Category.NPCS, write=True)
    # eb.scrape_entities(Category.BOSSES, write=True)

    # eb.scrape_entities(Category.ENEMIES, write=True)
    # eb.scrape_entities(Category.LOCATIONS, write=True)
    # eb.scrape_entities(Category.LEGACY_DUNGEONS, write=True)

    # eb.scrape_entities(Category.ITEMS, write=True)
    # eb.scrape_entities(Category.TALISMANS, write=True)
    # eb.scrape_entities(Category.SPIRIT_ASH, write=True)
    # eb.scrape_entities(Category.SPELLS, write=True)

    # eb.scrape_entities(Category.SKILLS, write=True)

    # eb.scrape_entity("Alberich's Set", Category.ARMOR, True)
    # eb.scrape_entity("Alberich's Pointed Hat", Category.ARMOR, True)
    # eb.scrape_entity("All-Knowing Set", Category.ARMOR, True)
    # eb.scrape_entity("Bloodhound Knight Armor (Altered)", Category.ARMOR, True)
    # eb.scrape_entity("Rotten Duelist Greaves", Category.ARMOR, True)
    # eb.scrape_entity("Gravekeeper Cloak", Category.ARMOR, True)
    # eb.scrape_entity("Crucible Tree Helm", Category.ARMOR, True)
    # eb.scrape_entity("Twinned Set", Category.ARMOR, True)
    # eb.scrape_entity("Royal Remains Armor", Category.ARMOR, True)
    # eb.scrape_entity("Chain Leggings", Category.ARMOR, True)
    # eb.scrape_entity("Hierodas Glintstone Crown", Category.ARMOR, True)
    # eb.scrape_entity("Raging Wolf Gauntlets", Category.ARMOR, True)
    # eb.scrape_entity("Drake Knight Set", Category.ARMOR, True)
    # eb.scrape_entity("Bandit Set", Category.ARMOR, True)
    # eb.scrape_entity("Old Aristocrat Set", Category.ARMOR, True)
    # eb.scrape_entity("Banished Knight Armor (Altered)", Category.ARMOR, True)
    # eb.scrape_entity("Blue Silver Set", Category.ARMOR, True)
    # eb.scrape_entity("Tree Sentinel Set", Category.ARMOR, True)
    # eb.scrape_entity("Preceptor's Set", Category.ARMOR, True)
    # eb.scrape_entity("Raging Wolf Set", Category.ARMOR, True)
    # eb.scrape_entity("War Surgeon Set", Category.ARMOR, True)
    # eb.scrape_entity("Diallos's Mask", Category.ARMOR, True)
    # eb.scrape_entity("Ivory-Draped Tabard", Category.ARMOR, True)
    # eb.scrape_entity("Twinsage Glintstone Crown", Category.ARMOR, True)
    # eb.scrape_entity("Ragged Set", Category.ARMOR, True)
    # eb.scrape_entity("Prophet Set", Category.ARMOR, True)
    # eb.scrape_entity("Brave's Set", Category.ARMOR, True)
    # eb.scrape_entity("Sorcerer Manchettes", Category.ARMOR, True)
    # eb.scrape_entity("Fur Leggings", Category.ARMOR, True)
    # eb.scrape_entity("Scaled Helm", Category.ARMOR, True)

    # eb.scrape_entity("Cipher Pata", Category.WEAPONS, True)
    # eb.scrape_entity("Beastclaw Greathammer", Category.WEAPONS, True)
    # # eb.scrape_entity("Noble's Estoc", Category.WEAPONS, True)
    # eb.scrape_entity("Nox Flowing Sword", Category.WEAPONS, True)
    # eb.scrape_entity("Nox Flowing Hammer", Category.WEAPONS, True)

    # eb.scrape_entity("Aspects of the Crucible: Breath", Category.SPELLS, True)
    # eb.scrape_entity("Aspects of the Crucible: Horns", Category.SPELLS, True)
    # eb.scrape_entity("Aspects of the Crucible: Tail", Category.SPELLS, True)
    # eb.scrape_entity("Flame Fall Upon Them", Category.SPELLS, True)
    # eb.scrape_entity("Flame, Grant Me Strength", Category.SPELLS, True)
    # eb.scrape_entity("Gelmir's Fury", Category.SPELLS, True)
    # eb.scrape_entity("Black Flame's Protection", Category.SPELLS, True)
    # eb.scrape_entity("Aspects of the Crucible: Horns", Category.SPELLS, True)

    # eb.scrape_entity("Aspect of the Crucible: Breath", Category.SPELLS, True)

    # eb.scrape_entity("Abandoned Merchant's Bell Bearing", Category.ITEMS, True)
    # eb.scrape_entity("Meeting Place Map", Category.ITEMS, True)
    # eb.scrape_entity("Academy Glintstone Key", Category.ITEMS, True)
    # eb.scrape_entity("Ritual Pot", Category.ITEMS, True)
    # eb.scrape_entity("Boiled Crab", Category.ITEMS, True)
    # eb.scrape_entity("Smithing-Stone Miner's Bell Bearing (1)", Category.ITEMS, True)
    # eb.scrape_entity("Crimson Bubbletear", Category.ITEMS, True)
    # eb.scrape_entity("Arteria Leaf", Category.ITEMS, True)
    # eb.scrape_entity("Sewing Needle", Category.ITEMS, True)
    # eb.scrape_entity("Eye of Yelough", Category.ITEMS, True)
    # eb.scrape_entity("Kalé's Bell Bearing", Category.ITEMS, True)
    # eb.scrape_entity("Fire Arrow", Category.ITEMS, True)
    # eb.scrape_entity("Note: Stonedigger Trolls", Category.ITEMS, True)
    # eb.scrape_entity("Sleepbone Arrow (Fletched)", Category.ITEMS, True)
    # eb.scrape_entity("Cuckoo Glintstone", Category.ITEMS, True)
    # eb.scrape_entity("St. Trina's Arrow", Category.ITEMS, True)
    # eb.scrape_entity("Kale's Bell Bearing", Category.ITEMS, True)
    # eb.scrape_entity("Miquella's Lily", Category.ITEMS, True)
    # eb.scrape_entity("Deathroot", Category.ITEMS, True)
    # eb.scrape_entity("Fire Monks' Prayerbook", Category.ITEMS, True)
    # eb.scrape_entity("Smithing-Stone Miner's Bell Bearing (3)", Category.ITEMS, True)
    # eb.scrape_entity("Somberstone Miner's Bell Bearing (1)", Category.ITEMS, True)
    # eb.scrape_entity("Nomadic Merchant's Bell Bearing (9)", Category.ITEMS, True)
    # eb.scrape_entity("Armorer's Cookbook (6)", Category.ITEMS, True)
    # eb.scrape_entity("Shabriri Grape", Category.ITEMS, True)
    # eb.scrape_entity("Grace Mimic", Category.ITEMS, True)
    # eb.scrape_entity("Rune Arc", Category.ITEMS, True)
    

    # eb.scrape_entity("Ancestral Spirit's Horn", Category.TALISMANS, True)
    # eb.scrape_entity("Assassin's Crimson Dagger", Category.TALISMANS, True)

    # eb.scrape_entity("Ancient Dragon Knight Kristoff Ashes", Category.SPIRIT_ASH, True)
    # eb.scrape_entity("Dolores the Sleeping Arrow Puppet", Category.SPIRIT_ASH, True)
    # eb.scrape_entity("Mausoleum Soldier Ashes", Category.SPIRIT_ASH, True)



    # eb.scrape_entity("Radagon of the Golden Order", Category.BOSSES, True)
    # eb.scrape_entity("Omenkiller", Category.BOSSES, True)
    # eb.scrape_entity("Flying Dragon Agheel", Category.BOSSES, True)
    # eb.scrape_entity("Black Blade Kindred", Category.BOSSES, True)
    # eb.scrape_entity("Cleanrot Knight", Category.BOSSES, True)
    # eb.scrape_entity("Dragonkin Soldier", Category.BOSSES, True)
    # eb.scrape_entity("Beast Clergyman", Category.BOSSES, True)
    # eb.scrape_entity("Grafted Scion", Category.BOSSES, True)
    # eb.scrape_entity("Black Knife Assassin", Category.BOSSES, write=True)
    # eb.scrape_entity("Godskin Apostle", Category.BOSSES, write=True)
    # eb.scrape_entity("Loretta, Knight of the Haligtree", Category.BOSSES, write=True)
    # eb.scrape_entity("Margit, the Fell Omen", Category.BOSSES, write=True)
    # eb.scrape_entity("Demi-Human Queen Maggie", Category.BOSSES, write=True)
    # eb.scrape_entity("Demi-Human Queen Gilika", Category.BOSSES, write=True)
    # eb.scrape_entity("Demi-Human Queen Margot", Category.BOSSES, write=True)

    # eb.scrape_entity("Roundtable Hold", Category.LOCATIONS, True)
    # eb.scrape_entity("Abandoned Cave", Category.LOCATIONS, True)
    # eb.scrape_entity("Ainsel River", Category.LOCATIONS, True)
    # eb.scrape_entity("Guardians' Garrison", Category.LOCATIONS, True)
    # eb.scrape_entity("Liurnia of the Lakes", Category.LOCATIONS, True)
    # eb.scrape_entity("Laskyar Ruins", Category.LOCATIONS, True)
    # eb.scrape_entity("Ordina, Liturgical Town", Category.LOCATIONS, True)
    # eb.scrape_entity("Weeping Peninsula", Category.LOCATIONS, True)
    # eb.scrape_entity("Altus Plateau", Category.LOCATIONS, True)
    # eb.scrape_entity("Cathedral of the Forsaken", Category.LOCATIONS, True)
    # eb.scrape_entity("Cathedral of Dragon Communion (Caelid)", Category.LOCATIONS, True)
    # eb.scrape_entity("Mountaintops of the Giants", Category.LOCATIONS, True)
    # eb.scrape_entity("Leyndell, Capital of Ash", Category.LOCATIONS, True)
    # eb.scrape_entity("Cathedral of Dragon Communion", Category.LOCATIONS, True)
    # eb.scrape_entity("Consecrated Snowfield", Category.LOCATIONS, True)
    # eb.scrape_entity("Wandering Mausoleum", Category.LOCATIONS, True)
    # eb.scrape_entity("Mt Gelmir", Category.LOCATIONS, True)

    # eb.scrape_entity("Teardrop Scarab", Category.ENEMIES, True)
    # eb.scrape_entity("Depraved Perfumer", Category.ENEMIES, write=True)
    # eb.scrape_entity("Giant Crab", Category.ENEMIES, write=True)
    # eb.scrape_entity("Giant Bat", Category.ENEMIES, write=True)
    # eb.scrape_entity("Lesser Alabaster Lord", Category.ENEMIES, write=True)
    # eb.scrape_entity("Tanith's Knight", Category.ENEMIES, write=True)
    # eb.scrape_entity("Albinauric", Category.ENEMIES, write=True)
    # eb.scrape_entity("Necromancer", Category.ENEMIES, write=True)
    # eb.scrape_entity("Skeletons", Category.ENEMIES, write=True)
    # eb.scrape_entity("Slug", Category.ENEMIES, write=True)
    # eb.scrape_entity("Springhare", Category.ENEMIES, write=True)
    # eb.scrape_entity("Baleful Shadow", Category.ENEMIES, write=True)
    # eb.scrape_entity("Giant Land Octopus", Category.ENEMIES, write=True)
    # eb.scrape_entity("Land Octopus", Category.ENEMIES, write=True)

    # eb.scrape_entity("Blaidd", Category.NPCS, True)
    # eb.scrape_entity("Hyetta", Category.NPCS, True)
    # eb.scrape_entity("Goldmask", Category.NPCS, True)
    # eb.scrape_entity("Diallos", Category.NPCS, True)
    # eb.scrape_entity("Bloody Finger Hunter Yura", Category.NPCS, True)
    # eb.scrape_entity("Brother Corhyn", Category.NPCS, True)
    # eb.scrape_entity("Tanith", Category.NPCS, True)
    # eb.scrape_entity("Fia", Category.NPCS, True)
    # eb.scrape_entity("Abandoned Merchant Siofra River", Category.NPCS, True)
    # eb.scrape_entity("Ranni the Witch", Category.NPCS, write=True)
    # eb.scrape_entity("Renna", Category.NPCS, write=True)
    # eb.scrape_entity("Rennala, Queen of the Full Moon (NPC)", Category.NPCS, write=True)
    # eb.scrape_entity("Preceptor Seluvis", Category.NPCS, write=True)
    # eb.scrape_entity("Sanguine Noble (NPC)", Category.NPCS, write=True)
    # eb.scrape_entity("Two Fingers", Category.NPCS, write=True)
    # eb.scrape_entity("War Counselor Iji", Category.NPCS, write=True)
    # eb.scrape_entity("White Mask Varré", Category.NPCS, write=True)
    # eb.scrape_entity("Iron Fist Alexander", Category.NPCS, write=True)
    # eb.scrape_entity("Gideon Ofnir", Category.NPCS, write=True)
    # eb.scrape_entity("Gurranq Beast Clergyman", Category.NPCS, write=True)
    # eb.scrape_entity("Torrent (Spirit Steed)", Category.NPCS, write=True)
    # eb.scrape_entity("Eleonora, Violet Bloody Finger", Category.NPCS, write=True)
    # eb.scrape_entity("Renna", Category.NPCS, write=True)
    # eb.scrape_entity("Dung Eater", Category.NPCS, write=True)
    # eb.scrape_entity("Volcano Manor Spirit", Category.NPCS, write=True)
    # eb.scrape_entity("Melina", Category.NPCS, write=True)
    # eb.scrape_entity("Kingsrealm Spirit", Category.NPCS, write=True)

    # eb.scrape_entity("Unblockable Blade Skill", Category.SKILLS, write=True)

    # Examples - Everything but Description truncated
    # eb.scrape_entity("Hawk Crest Wooden Shield", Category.SHIELDS, True)
    # eb.scrape_entity("Ice Crest Shield", Category.SHIELDS, True)
    # eb.scrape_entity("Wooden Greatshield", Category.SHIELDS, True)
    # eb.scrape_entity("Distinguished Greatshield", Category.SHIELDS, True)
    # eb.scrape_entity("Pillory Shield", Category.SHIELDS, True)
    # eb.scrape_entity("Cuckoo Greatshield", Category.SHIELDS, True)
    
    # Examples - No Description
    # eb.scrape_entity("Spiked Palisade Shield", Category.SHIELDS, True)
    # eb.scrape_entity("Visage Shield", Category.SHIELDS, True)

    # Examples - Extra <em>s getting into Description
    # eb.scrape_entity("Academy Glintstone Staff", Category.WEAPONS, True)
    # eb.scrape_entity("Albinauric Staff", Category.WEAPONS, True)
    # eb.scrape_entity("Azur's Glintstone Staff", Category.WEAPONS, True)
    # eb.scrape_entity("Miquellan Knight's Sword", Category.WEAPONS, True)

    # Examples - Last line of Description not parsed correctly
    # eb.scrape_entity("Battle Hammer", Category.WEAPONS, True)
    # eb.scrape_entity("Beast-Repellent Torch", Category.WEAPONS, True)
    # eb.scrape_entity("Beastman's Cleaver", Category.WEAPONS, True)

    # Example - Useless/bad linking to entities in bullets after "Sell Value""
    # eb.scrape_entity("Albinauric Bow", Category.WEAPONS, True)
    # eb.scrape_entity("Alabaster Lord's Sword", Category.WEAPONS, True)
    # eb.scrape_entity("Azur's Glintstone Staff", Category.WEAPONS, True) # Needs targeted fix
    # eb.scrape_entity("Bloodhound's Fang", Category.WEAPONS, True)

    # Example - Bad links
    # eb.scrape_entity("Executioner's Greataxe", Category.WEAPONS, True)
    # eb.scrape_entity("Zweihander", Category.WEAPONS, True)

    # Example - No spaces between sentences separated by a <br>
    # eb.scrape_entity("Dragon Communion Seal", Category.WEAPONS, True)

    # Example - Remaining Video link
    # eb.scrape_entity("Dragon Halberd", Category.WEAPONS, True)

    # Example - Description not fully italicized
    # eb.scrape_entity("Duelist Greataxe", Category.WEAPONS, True) # Includes strange page split

    # eb.scrape_entity("Erdtree Seal", Category.WEAPONS, True) # Includes strange page split

    # eb.scrape_entity("Wraith Calling Bell", Category.WEAPONS, True)

    # eb.scrape_entity("Wing of Astel", Category.WEAPONS, True)

    # eb.scrape_entity("Varre's Bouquet", Category.WEAPONS, True)

    # eb.scrape_entity("Urumi", Category.WEAPONS, True)

    # eb.scrape_entity("Troll's Golden Sword", Category.WEAPONS, True)

    # eb.scrape_entity("Troll Knight's Sword", Category.WEAPONS, True)

    # eb.scrape_entity("Arbalest", Category.WEAPONS, True)

    # eb.scrape_entity("Bandit's Curved Sword", Category.WEAPONS, True)

    # Example - Everything after Description truncated
    # eb.scrape_entity("Black Bow", Category.WEAPONS, True)

    # Example - Get cut off either in the middle of the Description, or everything after is truncated
    # eb.scrape_entity("Bastard's Stars", Category.WEAPONS, write=True)

    # eb.prepare_entity('Dagger', Category.WEAPONS)
    # eb.scrape_entity('Dagger', Category.WEAPONS)
    # eb.write_entity('Dagger')
    # print(eb[Category.WEAPONS][0])

    # logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
    # log = logging.getLogger('elden-bring-logger')

    # scraper = Scraper(log)

    # eb.prepare_entities('Talismans')
    # talismans_names = eb.get_entity_names('Talismans')
    # eb.scrape_entities('Talismans')

    # print(talismans_names)
    # print(eb['Talismans'][0])
    # print(len(eb['Talismans']))

    # eb.prepare_entities(Category.SKILLS)
    # eb.scrape_entities(Category.SKILLS)
    # print(eb[Category.SKILLS])

    # eb.prepare_entities(Category.WEAPONS, 1)
    # weapon_names = eb.get_entity_names(Category.WEAPONS)
    # print(weapon_names)
    # eb.scrape_entities(Category.WEAPONS)
    # eb.write_entities(Category.WEAPONS)

    # eb.prepare_entities(Category.SHIELD, 1)
    # shield_names = eb.get_entity_names(Category.SHIELD)
    # print(shield_names)
    # eb.scrape_entities(Category.SHIELD)
    # eb.write_entities(Category.SHIELD)
    

    # eb.prepare_entities(Category.LEGACY_DUNGEON)
    # legacy_dungeons_names = eb.get_entity_names(Category.LEGACY_DUNGEON)
    # eb.scrape_entity('Stormveil Castle', Category.LEGACY_DUNGEON)

    # print(eb['Legacy Dungeons'][0])

    # print(legacy_dungeons_names)
    # print(eb['Legacy Dungeons'][0])
    # print(len(eb['Legacy Dungeons']))

if __name__=="__main__":
    main()