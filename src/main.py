from elden_bring import *
from scraper import Scraper

from objects import *

def main():

    eb = EldenBring()

    # eb.scrape_entities(EntityCategory.WEAPONS, write=True)
    #eb.write_entities(EntityCategory.WEAPONS)

    # Examples - Extra <em>s getting into Description
    # eb.scrape_entity("Academy Glintstone Staff", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Albinauric Staff", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Azur's Glintstone Staff", EntityCategory.WEAPONS, True)

    # Examples - Last line of Description not parsed correctly
    # eb.scrape_entity("Battle Hammer", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Beast-Repellent Torch", EntityCategory.WEAPONS, True)
    # eb.scrape_entity("Beastman's Cleaver", EntityCategory.WEAPONS, True)

    # Example - <em> in the middle of the Description, after the G in "Given"
    # eb.scrape_entity("Banished Knight's Greatsword", EntityCategory.WEAPONS, True)
    eb.scrape_entity("Alabaster Lord's Sword", EntityCategory.WEAPONS, True)

    # Example - Malformed link
    # eb.scrape_entity("Black Knife", EntityCategory.WEAPONS, True)

    # Example - Last line of Description is not italicized
    # eb.scrape_entity("Battle Axe", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Wraith Calling Bell", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Wing of Astel", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Varre's Bouquet", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Urumi", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Troll's Golden Sword", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Troll Knight's Sword", EntityCategory.WEAPONS, True)

    # eb.scrape_entity("Arbalest", EntityCategory.WEAPONS, True)

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