from secret import api


heroes = api.get_heroes()


def MAX_ID():
    max_id = 0

    for hero in heroes["heroes"]:
        if hero["id"] > max_id:
            max_id = hero["id"]

    return(max_id +1)

heroes_array = [None] * MAX_ID()


class HERO(object):

    def __init__(self, _id, name):
        self.id = _id
        self.name = name


def heroes_order(heroes):

    for hero in heroes["heroes"]:
        hero_id = hero["id"]
        hero_name = hero["localized_name"]
        hero_object = HERO(hero_id, hero_name)
        heroes_array[(hero_id)] = hero_object

heroes_order(heroes)
