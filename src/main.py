from elden_bring import *
from scraper import Scraper

from objects import *

def main():

    eb = EldenBring()

    eb.prepare_entity('Dagger', EntityCategory.WEAPONS)
    eb.scrape_entity('Dagger')
    eb.write_entity('Dagger')
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