from elden_bring import *

def main():

    eb = EldenBring()

    # eb.create_skills() # WORKS
    eb.create_hidden() # WORKS
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
    
    
    # dagger = Parser.url_to_entity(WIKI_BASE_URL+"/Dagger", EntityType.WEAPON, force_download_image=False)
    # print(dagger)
    # dagger.write_to_file()

    # item = parse_endpoint_to_entity(WIKI_BASE_URL+"/Fingerslayer+Blade", force_download_image=False)
    # item = parse_endpoint_to_entity(WIKI_BASE_URL+"/Miquellan+Knight's+Sword", force_download_image=False)
    
    # giant_crusher = parse_endpoint_to_entity(WIKI_BASE_URL+"/Giant-Crusher", EntityType.WEAPON, force_download_image=False)
    # print(giant_crusher)
    # giant_crusher.write_to_file()

    # Cleanrot Knight's Sword
    # cleanrot_knights_sword = Parser.url_to_entity(WIKI_BASE_URL+"/Cleanrot+Knight's+Sword", EntityType.WEAPON, force_download_image=False)
    # print(cleanrot_knights_sword)
    # cleanrot_knights_sword.write_to_file()

    # ALABASTER LORD'S SWORD
    # alabaster_lords_sword = Parser.url_to_entity(WIKI_BASE_URL+"/Alabaster+Lord's+Sword", EntityType.WEAPON, force_download_image=False)
    # print(alabaster_lords_sword)
    # alabaster_lords_sword.write_to_file()

    # Parrying Dagger
    # parrying_dagger = Parser.url_to_entity(WIKI_BASE_URL+"/Parrying+Dagger", EntityType.WEAPON, force_download_image=False)
    # print(parrying_dagger)
    # parrying_dagger.write_to_file()

    # Torch
    # torch = Parser.url_to_entity(WIKI_BASE_URL+"/Torch", EntityType.WEAPON, force_download_image=False)
    # print(torch)
    # torch.write_to_file()

if __name__=="__main__":
    main()