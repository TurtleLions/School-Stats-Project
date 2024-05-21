import constants
import requests
import pandas as pd
import random
api_key = constants.api_key

def main():
  all_sampled_ids = []
  new_player_list = []
  experienced_player_list = []
  while len(new_player_list) < 5000 or len(experienced_player_list) < 5000:
    random_list = random.sample(range(1000000000, 1099999999), 100)
    test_list = [i for i in random_list if i not in all_sampled_ids]
    removed_list = [i for i in random_list if i in all_sampled_ids]
    print("Test List: " + str(test_list))
    print("Removed List: " + str(removed_list))

    temp_new_player_list, temp_experienced_player_list = stats_search(test_list)
    all_sampled_ids.extend(test_list)
    new_player_list.extend(temp_new_player_list)
    experienced_player_list.extend(temp_experienced_player_list)
    print(str(len(new_player_list)) + " " + str(len(experienced_player_list)))

  print(str(all_sampled_ids))
  print(str(new_player_list))
  print(str(experienced_player_list))

  new_player_df = pd.DataFrame(new_player_list)
  experienced_player_df = pd.DataFrame(experienced_player_list)
  print(new_player_df)
  print(experienced_player_df)

  new_player_df.to_csv('new_player.csv')
  experienced_player_df.to_csv('experienced_player.csv')

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
  new_player_list = []
  experienced_player_list = []
  if response.status_code==200:
    responsejson = response.json()
    for account_id in account_ids:
      if(responsejson!=None and responsejson['data']!=None and responsejson['data'][str(account_id)]!=None and responsejson['data'][str(account_id)]['statistics']['all']['battles']>1000):
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
        if(responsejson['data'][str(account_id)]['statistics']['all']['battles']>5000):
          experienced_player_list.append(player)
        else:
          new_player_list.append(player)
  else:
      print(f"API Error: {response.status_code}")
  return new_player_list, experienced_player_list

main()