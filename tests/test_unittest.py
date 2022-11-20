from elden_bring import *



def test_1():
    assert 2 + 2 == 4

def test_entity_creation():
    eb = EldenBring()

    eb.scrape_entity('Dagger', EntityCategory.WEAPONS, write=False)

    assert eb[EntityCategory.WEAPONS][0].name == 'Dagger'