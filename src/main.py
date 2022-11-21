from elden_bring import *
from scraper import Scraper

from objects import *

def main():

    eb = EldenBring()

    # eb.create_hidden()

    # eb.scrape_entities(EntityCategory.WEAPONS, write=True)
    # eb.scrape_entities(EntityCategory.SHIELDS, write=True)
    # eb.scrape_entities(EntityCategory.ARMOR, write=True)
    # eb.scrape_entities(EntityCategory.NPCS, write=True)
    # eb.scrape_entities(EntityCategory.BOSSES, write=True)
    # eb.scrape_entities(EntityCategory.ENEMIES, write=True)
    # eb.scrape_entities(EntityCategory.LOCATIONS, write=True)

    # eb.scrape_entity("Alberich's Set", EntityCategory.ARMOR, True)
    # eb.scrape_entity("All-Knowing Set", EntityCategory.ARMOR, True)
    # eb.scrape_entity("Bloodhound Knight Armor (Altered)", EntityCategory.ARMOR, True)

    # eb.scrape_entity("Omenkiller", EntityCategory.BOSSES, True)
    # eb.scrape_entity("Flying Dragon Agheel", EntityCategory.BOSSES, True)
    # eb.scrape_entity("Black Blade Kindred", EntityCategory.BOSSES, True)
    # eb.scrape_entity("Cleanrot Knight", EntityCategory.BOSSES, True)
    # eb.scrape_entity("Dragonkin Soldier", EntityCategory.BOSSES, True)
    # eb.scrape_entity("Beast Clergyman", EntityCategory.BOSSES, True)

    # eb.scrape_entity("Abandoned Cave", EntityCategory.LOCATIONS, True)
    # eb.scrape_entity("Ainsel River", EntityCategory.LOCATIONS, True)
    # eb.scrape_entity("Guardians' Garrison", EntityCategory.LOCATIONS, True)
    eb.scrape_entity("Liurnia of the Lakes", EntityCategory.LOCATIONS, True)

    # eb.scrape_entity("Teardrop Scarab", EntityCategory.ENEMIES, True)

    # eb.scrape_entity("Hyetta", EntityCategory.NPCS, True)
    # eb.scrape_entity("Diallos", EntityCategory.NPCS, True)

    # Examples - Everything but Description truncated
    # eb.scrape_entity("Hawk Crest Wooden Shield", EntityCategory.SHIELDS, True)
    # eb.scrape_entity("Ice Crest Shield", EntityCategory.SHIELDS, True)
    # eb.scrape_entity("Wooden Greatshield", EntityCategory.SHIELDS, True)
    # eb.scrape_entity("Distinguished Greatshield", EntityCategory.SHIELDS, True)
    # eb.scrape_entity("Pillory Shield", EntityCategory.SHIELDS, True)
    
    # Examples - No Description
    # eb.scrape_entity("Spiked Palisade Shield", EntityCategory.SHIELDS, True)
    # eb.scrape_entity("Visage Shield", EntityCategory.SHIELDS, True)

    # Examples - Extra <em>s getting into Description
    # eb.scrape_entity("Academy Glintstone Staff", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Albinauric Staff", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Azur's Glintstone Staff", EntityCategory.WEAPONS, True)

    # Examples - Last line of Description not parsed correctly
    # eb.scrape_entity("Battle Hammer", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Beast-Repellent Torch", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Beastman's Cleaver", EntityCategory.WEAPONS, True)

    # Example - Useless/bad linking to entities in bullets after "Sell Value""
    # eb.scrape_entity("Albinauric Bow", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Alabaster Lord's Sword", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Azur's Glintstone Staff", EntityCategory.WEAPONS, True) # Needs targeted fix
    # eb.scrape_entity("Bloodhound's Fang", EntityCategory.WEAPONS, True)

    # Example - Bad links
    # eb.scrape_entity("Executioner's Greataxe", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Zweihander", EntityCategory.WEAPONS, True)

    # Example - No spaces between sentences separated by a <br>
    # eb.scrape_entity("Dragon Communion Seal", EntityCategory.WEAPONS, True)

    # Example - Remaining Video link
    # eb.scrape_entity("Dragon Halberd", EntityCategory.WEAPONS, True)

    # Example - Description not fully italicized
    # eb.scrape_entity("Duelist Greataxe", EntityCategory.WEAPONS, True) # Includes strange page split

    # eb.scrape_entity("Erdtree Seal", EntityCategory.WEAPONS, True) # Includes strange page split

    # eb.scrape_entity("Wraith Calling Bell", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Wing of Astel", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Varre's Bouquet", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Urumi", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Troll's Golden Sword", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Troll Knight's Sword", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Arbalest", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Bandit's Curved Sword", EntityCategory.WEAPONS, True)

    # Example - Everything after Description truncated
    # eb.scrape_entity("Black Bow", EntityCategory.WEAPONS, True)

    # Example - Get cut off either in the middle of the Description, or everything after is truncated
    # eb.scrape_entity("Bastard's Stars", EntityCategory.WEAPONS, write=True)

    # eb.prepare_entity('Dagger', EntityCategory.WEAPONS)
    # eb.scrape_entity('Dagger', EntityCategory.WEAPONS)
    # eb.write_entity('Dagger')
    #print(eb[EntityCategory.WEAPONS][0])

    # logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
    # log = logging.getLogger('elden-bring-logger')

    # scraper = Scraper(log)

    # eb.prepare_entities('Talismans')
    # talismans_names = eb.get_entity_names('Talismans')
    # eb.scrape_entities('Talismans')

    # print(talismans_names)
    # print(eb['Talismans'][0])
    # print(len(eb['Talismans']))

    # eb.prepare_entities(EntityCategory.SKILLS)
    # eb.scrape_entities(EntityCategory.SKILLS)
    # print(eb[EntityCategory.SKILLS])

    # eb.prepare_entities(EntityCategory.WEAPONS, 1)
    # weapon_names = eb.get_entity_names(EntityCategory.WEAPONS)
    # print(weapon_names)
    # eb.scrape_entities(EntityCategory.WEAPONS)
    # eb.write_entities(EntityCategory.WEAPONS)

    # eb.prepare_entities(EntityCategory.SHIELD, 1)
    # shield_names = eb.get_entity_names(EntityCategory.SHIELD)
    # print(shield_names)
    # eb.scrape_entities(EntityCategory.SHIELD)
    # eb.write_entities(EntityCategory.SHIELD)
    

    # eb.prepare_entities(EntityCategory.LEGACY_DUNGEON)
    # legacy_dungeons_names = eb.get_entity_names(EntityCategory.LEGACY_DUNGEON)
    # eb.scrape_entity('Stormveil Castle', EntityCategory.LEGACY_DUNGEON)

    # print(eb['Legacy Dungeons'][0])

    # print(legacy_dungeons_names)
    # print(eb['Legacy Dungeons'][0])
    # print(len(eb['Legacy Dungeons']))

if __name__=="__main__":
    main()