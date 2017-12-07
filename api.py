import urllib.parse
from pprint import pprint

import requests
from flask import json

from config import SUMMONER_DATA_URL, API_BASE, API_KEY, MATCH_HISTORY_URL, MATCH_DATA_URL, SPELL_STATIC_URL, \
    CHAMPIONS_STATIC_URL, ITEMS_STATIC_URL


def get_static_data(static_url):
    r = requests.get(API_BASE + static_url, params={'api_key': API_KEY})
    if r.status_code == 429:
        if 'summoner' in static_url:
            data = json.load(open('lol_data/summoner_spells.json'))
            result = {}
            for item in data['data'].values():
                result[item['id']] = item['name']

            return result
        elif 'items' in static_url:
            data = json.load(open('lol_data/items.json'))
            result = {}
            for item in data['data'].values():
                result[item['id']] = item['name']

            return result
        elif 'champions' in static_url:
            data = json.load(open('lol_data/champions.json'))
            result = {}
            for item in data['data'].values():
                result[item['id']] = item['name']

            return result
    result = {}
    data = r.json()
    for item in data['data'].values():
        result[item['id']] = item['name']

    return result


spell_id_name_map = get_static_data(SPELL_STATIC_URL)
# champ_id_name_map = get_static_data(CHAMPIONS_STATIC_URL)
item_id_name_map = get_static_data(ITEMS_STATIC_URL)


def get_account_info(summoner_name):
    r = requests.get(API_BASE + SUMMONER_DATA_URL.format(summonerName=urllib.parse.quote(summoner_name)),
                     params={'api_key': API_KEY})
    result = r.json()
    return result


def get_match_list(account_id):
    r = requests.get(API_BASE + MATCH_HISTORY_URL.format(accountId=account_id), params={'api_key': API_KEY})
    result = r.json()
    return result


def get_participant_id(account_id, participant_identities):
    for identity in participant_identities:
        if identity['player']['accountId'] == account_id:
            return int(identity['participantId'])
    return -1


def get_match_data(account_id, match_id):
    r = requests.get(API_BASE + MATCH_DATA_URL.format(matchId=match_id), params={'api_key': API_KEY})
    match_data = r.json()

    participant_id = get_participant_id(account_id, match_data['participantIdentities'])
    player_data = match_data['participants'][participant_id - 1]

    result = {
        'championId': player_data['championId'],
        'outcome': "Won" if player_data['stats']['win'] else "Lost",
        'summonerSpells': [player_data['spell1Id'], player_data['spell2Id']],
        'gameDuration': match_data['gameDuration'],
        'kda': '{kills}:{deaths}:{assists}'.format(kills=player_data['stats']['kills'],
                                                   deaths=player_data['stats']['deaths'],
                                                   assists=player_data['stats']['assists']),
        'items': [player_data['stats']['item0'], player_data['stats']['item1'], player_data['stats']['item2'],
                  player_data['stats']['item3'], player_data['stats']['item4'], player_data['stats']['item5'],
                  player_data['stats']['item6']],

        'creepsPerMinute': '{:.2f}'.format(
            sum([float(x) for x in player_data['timeline']['creepsPerMinDeltas'].values()]) / 4)
    }
    for i, item in enumerate(result['items']):
        result['items'][i] = item_id_name_map.get(item, 'UNK')

    for i, spell in enumerate(result['summonerSpells']):
        result['summonerSpells'][i] = spell_id_name_map[spell]

    return result




def get_all_player_data(summoner_name):
    account_data = get_account_info(summoner_name)
    account_id = account_data['accountId']
    level = account_data['summonerLevel']

    match_history = get_match_list(account_id)

    return  {
        "matchData": [get_match_data(account_id, match["gameId"]) for match in match_history["matches"]]
    }


if __name__ == '__main__':
    pprint(get_all_player_data('BFY Meowington'))