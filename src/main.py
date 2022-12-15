from elden_brain import *
from scraper import Scraper

from objects import *

def main():

    eb = EldenBrain() # Optionally provide cached Vault location, otherwise used config

    # print(eb.getCategories())
    print(eb.getNamesByCategory('Spirit Ashes'))

    # eb.create(category='Armor')
    # eb.create(category='Hidden')
    # eb.create(category='Legacy Dungeons')
    # eb.create(category='Locations')
    # eb.create(category='NPCs')
    # eb.create(category='Shields')
    # eb.create(category='Skills')
    # eb.create(category='Spells')
    # eb.create(category='Spirit Ashes')
    # eb.create(category='Talismans')
    # eb.create(category='Weapons')

    # eb.create()

    # eb.create('Dagger', 'Weapons')
    # eb.create('Frenzied Flame Seal', 'Weapons')
    # eb.create('Carian Glintstone Staff', 'Weapons')
    # eb.create('Vulgar Militia Saw', 'Weapons')
    # eb.create("Executioner's Greataxe", 'Weapons')

    # eb.create('Miranda Sprout', 'Creatures and Enemies')
    # eb.create('Celebrant', 'Creatures and Enemies')
    # eb.create('Putrid Corpse', 'Creatures and Enemies')

    # eb.create('Beast Clergyman', 'Bosses')
    # eb.create("Fia's Champions", 'Bosses')
    # eb.create('Fallingstar Beast', 'Bosses')
    # eb.create('Ulcerated Tree Spirit', 'Bosses')
    # eb.create('Margit, the Fell Omen', 'Bosses')
    

    # eb.create('Roderika', category='NPCs')

    # eb.create('Crumbling Farum Azula', category='Legacy Dungeons')
    # eb.create('Volcano Manor', category='Legacy Dungeons')

    # eb.create('Arrow', category='Items/Arrows and Bolts')

    # eb.create('Purifying Crystal Tear', category='Items/Crystal Tears')

    # eb.create('Dragon Cult Prayerbook', category='Items/Key Items')

    # eb.create("Adula's Moonblade", category='Spells')

    # eb.create('Godrick Foot Soldier Set', category='Armor/Armor Sets')
    # eb.create('Nox Monk Bracelets', category='Armor/Armor Sets')
    # eb.create('Commoners of the Lands Between Set', category='Armor/Armor Sets')
    # eb.create('Crucible Tree Set', category='Armor/Armor Sets')
    # eb.create('House Marais Set', category='Armor/Armor Sets')
    # eb.create("Alberich's Set", category='Armor/Armor Sets')

    # eb.create("Diallos's Mask", category='Armor/Helms')
    # eb.create('Octopus Head', category='Armor/Helms')

    # eb.create("Alberich's Robe", category='Armor/Chest Armor')

    # eb.create("Alberich's Trousers", category='Armor/Leg Armor')
    
    # eb.create('Cracked Pot', category='Items/Key Items')
    # eb.create('Cursemark of Death', category='Items/Key Items')



if __name__=="__main__":
    main()