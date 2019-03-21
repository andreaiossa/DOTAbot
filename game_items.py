from secret import api

items = api.get_game_items()

class ITEM(object):

    def __init__(self, _id, name):
        self.id = _id
        self.name = name


def MAX_ID():
    max_id = 0

    for item in items["items"]:
        if item["id"] > max_id:
            max_id = item["id"]

    return(max_id +1)


item_array = [None] * MAX_ID()



def item_order(items):

    for item in items["items"]:
        item_id = item["id"]
        item_name = item["localized_name"]
        item_object = ITEM(item_id, item_name)
        item_array[(item_id)] = item_object

item_order(items)
