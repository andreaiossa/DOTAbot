from secret import api
from game_items import item_array
from game_heroes import heroes_array



match = api.get_match_details("3519079939")

player = match["players"]

player[0]


print(api.get_match_history(account_id=76561198053472580))
