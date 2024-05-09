import constants
import requests
import pandas as pd
import random
api_key = constants.api_key
battle_count_min = 5000

def main():
  all_sampled_player_list = []
  while len(all_sampled_player_list) < 10:
    list = random.sample(range(1000000000, 1099999999), 100)
    all_sampled_player_list.extend(stats_search(list))
    print(len(all_sampled_player_list))
  print(all_sampled_player_list)
  df = pd.DataFrame(all_sampled_player_list)
  print(df)

def stats_search(account_ids):
  api_url = 'https://api.wotblitz.com/wotb/account/info/'
  accountstr = ""
  for account_id in account_ids:
    accountstr = accountstr+str(account_id)+','
  params = {
      'application_id': api_key,
      'account_id': accountstr,
  }
  response = requests.get(api_url, params=params)
  player_list = []
  if response.status_code==200:
    responsejson = response.json()
    for account_id in account_ids:
      if(responsejson['data'][str(account_id)]!=None and responsejson['data'][str(account_id)]['statistics']['all']['battles']>5000):
        spotted = responsejson['data'][str(account_id)]['statistics']['all']['spotted']
        hits = responsejson['data'][str(account_id)]['statistics']['all']['hits']
        frags = responsejson['data'][str(account_id)]['statistics']['all']['frags']
        wins = responsejson['data'][str(account_id)]['statistics']['all']['wins']
        losses = responsejson['data'][str(account_id)]['statistics']['all']['losses']
        battles = responsejson['data'][str(account_id)]['statistics']['all']['battles']
        damage_dealt = responsejson['data'][str(account_id)]['statistics']['all']['damage_dealt']
        damage_received = responsejson['data'][str(account_id)]['statistics']['all']['damage_received']
        shots = responsejson['data'][str(account_id)]['statistics']['all']['shots']
        xp = responsejson['data'][str(account_id)]['statistics']['all']['xp']
        win_and_survived = responsejson['data'][str(account_id)]['statistics']['all']['win_and_survived']
        survived_battles = responsejson['data'][str(account_id)]['statistics']['all']['survived_battles']
        player = {'account_id': account_id, 'spotted': spotted, 'hits': hits, 'frags': frags, 'wins': wins, 'losses': losses, 'battles': battles, 'damaged_dealt': damage_dealt, 'damaged_received': damage_received, 'shots': shots, 'xp': xp, 'win_and_survived': win_and_survived, 'survived_battles': survived_battles}
        player_list.append(player)
  else:
      print(f"API Error: {response.status_code}")
  return player_list

main()