from elden_bring import *
from scraper import Scraper

def main():

    eb = EldenBring()

    # logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
    # log = logging.getLogger('elden-bring-logger')

    # scraper = Scraper(log)

    eb.prepare_entities('Talismans')
    talismans_names = eb.get_entity_names('Talismans')
    eb.scrape_entities('Talismans')

    # print(talismans_names)
    print(eb['Talismans'][0])
    print(len(talismans_entities))

    # eb.create_skills() # WORKS
    # eb.create_hidden() # WORKS
    # eb.create_weapons() # WORKS
    # eb.create_shields() # WORKS
    # eb.create_armor()
    # eb.create_locations() # WORKS
    # eb.create_legacy_dungeons() # NEEDS SPECIAL PAGE PARSING
    # eb.create_spells() # WORKS
    # eb.create_spirit_ashes()
    # eb.create_creatures_and_enemies() # WORKS
    # eb.create_bosses()
    # eb.create_npcs() # WORKS
    # eb.create_talismans()

    # Create destination directory if it doesn't exist
    # if not os.path.exists(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY):
    #     os.mkdir(CACHE_LOCATION + VAULT_NAME + IMAGE_WRITE_DIRECTORY)

    # all_endpoints = get_all_endpoints()

    # all_item_urls = Parser.get_items_urls()
    # print(all_item_urls)
    # print(len(all_item_urls))
    # f = open(CACHE_LOCATION + VAULT_NAME + 'temp.txt', 'w')
    # f.write('\n'.join(list(set(all_item_urls))))
    # f.close()
    # Parser.convert_urls_to_entities(all_item_urls, EntityType.ITEM)

    # all_legacy_dungeon_urls = Parser.get_legacy_dungeon_urls()
    # print(all_legacy_dungeon_urls)

    # all_weapon_urls = Parser.get_weapons_urls()
    # Parser.convert_urls_to_entities(all_weapon_urls, EntityType.WEAPON)

    # all_location_urls = Parser.get_location_urls()
    # print(len(all_location_urls))
    # Parser.convert_urls_to_entities(all_location_urls, EntityType.LOCATION)

    # f = open(CACHE_LOCATION + VAULT_NAME + 'temp.txt', 'w')
    # f.write('\n'.join(list(set(all_location_urls))))
    # f.close()
    # print(all_location_urls)

    ## NPCS
    # all_npcs_urls = Parser.get_npcs_urls()
    # print(all_npcs_urls)
    # print(len(all_npcs_urls))
    # Parser.convert_urls_to_entities(all_npcs_urls, EntityType.NPC)

    # Dagger
    # dagger = scraper.url_to_entity("/Dagger", EntityType.WEAPON, force_image_download=False)
    # print(dagger)
    # dagger.write()

    # Gravel Stone Seal
    # gravel_stone_seal = scraper.url_to_entity("/Gravel+Stone+Seal", EntityType.WEAPON, force_image_download=False)
    # print(gravel_stone_seal)
    # gravel_stone_seal.write()

if __name__=="__main__":
    main()