import dota2api
import discord
from steam import steamid
from validators import url as is_a_URL

api = dota2api.Initialise("key value", raw_mode = False)


def id_64(value):
    if is_a_URL(value):
        finale_id = steamid.steam64_from_url(value, http_timeout=30)

    else:
        if isinstance(value, str):
            if "STEAM" in value:
                accountID = steamid.steam2_to_tuple(value)[0]
                Steam_Id = steamid.SteamID(accountID)
                finale_id = Steam_Id.as_64

            elif "[U" in value:
                accountID = steamid.steam3_to_tuple(value)[0]
                Steam_Id = steamid.SteamID(accountID)
                finale_id = Steam_Id.as_64

            else:
                possible_URL = 'https://steamcommunity.com/id/{}/'.format(value)
                finale_id = steamid.steam64_from_url(possible_URL, http_timeout=30)

        elif isinstance(value, int):
            finale_id =  value

    return finale_id
