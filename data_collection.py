import constants
import requests
import pandas as pd
import random
import threading
import time
import itertools
api_key = constants.api_key
MIN_SAMPLE_SIZE = 5000

all_sampled_ids = []

new_player_list = []
experienced_player_list = []

last_time = time.time()
last_hour_time = time.time()

def main():
  global MIN_SAMPLE_SIZE
  global all_sampled_ids
  global new_player_list
  global experienced_player_list
  global last_time
  global last_hour_time

  while len(new_player_list) < MIN_SAMPLE_SIZE or len(experienced_player_list) < MIN_SAMPLE_SIZE:
    new_time = time.time()
    if new_time>= last_time+1:
      if new_time>= last_hour_time+(60*60):
        last_hour_time = new_time
        new_player_df = pd.DataFrame(new_player_list)
        experienced_player_df = pd.DataFrame(experienced_player_list)
        print(new_player_df)
        print(experienced_player_df)

        new_player_df.to_csv('new_player.csv')
        experienced_player_df.to_csv('experienced_player.csv')
        
      last_time = new_time
      t1 = threading.Thread(target=random_UID_generation, args=())
      t2 = threading.Thread(target=random_UID_generation, args=())
      t3 = threading.Thread(target=random_UID_generation, args=())
      t4 = threading.Thread(target=random_UID_generation, args=())
      t5 = threading.Thread(target=random_UID_generation, args=())
      t6 = threading.Thread(target=random_UID_generation, args=())
      t7 = threading.Thread(target=random_UID_generation, args=())
      t8 = threading.Thread(target=random_UID_generation, args=())
      t9 = threading.Thread(target=random_UID_generation, args=())
      t10 = threading.Thread(target=random_UID_generation, args=())

      t1.start()
      t2.start()
      t3.start()
      t4.start()
      t5.start()
      t6.start()
      t7.start()
      t8.start()
      t9.start()
      t10.start()

      t1.join()
      t2.join()
      t3.join()
      t4.join()
      t5.join()
      t6.join()
      t7.join()
      t8.join()
      t9.join()
      t10.join()

  print(str(all_sampled_ids))
  print(str(new_player_list))
  print(str(experienced_player_list))

  new_player_df = pd.DataFrame(new_player_list)
  experienced_player_df = pd.DataFrame(experienced_player_list)
  print(new_player_df)
  print(experienced_player_df)

  new_player_df.to_csv('new_player.csv')
  experienced_player_df.to_csv('experienced_player.csv')

def random_UID_generation():
  random_list = random.sample(range(1000000000, 1099999999), 100)
  test_list = list(set(random_list).difference(all_sampled_ids))
  removed_list = list(set(random_list).intersection(all_sampled_ids))
  print("Test List: " + str(test_list))
  print("Removed List: " + str(removed_list))
  temp_new_player_list, temp_experienced_player_list = stats_search(test_list)
  all_sampled_ids.extend(test_list)
  new_player_list.extend(temp_new_player_list)
  experienced_player_list.extend(temp_experienced_player_list)
  print(str(len(all_sampled_ids))+ " " + str(len(new_player_list)) + " " + str(len(experienced_player_list)))

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