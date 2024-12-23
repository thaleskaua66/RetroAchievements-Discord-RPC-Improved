import argparse
from colorama import Fore, Style, init
import configparser
from datetime import datetime
from pprint import pprint
from pypresence import Presence 
import re
import requests
import time
import os.path
import time
import warnings

global counter
global RPC
global rpcIsClosed
global temp1, temp2
global start_time

init(autoreset=True)

def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.RED + f"Failed to fetch data from {url}, status code: {response.status_code}")
        return None

def sanitize_console_name(console_name):
    sanitized_name = re.sub('[^0-9a-zA-Z]+', '', console_name)
    return sanitized_name.lower()

#RA Games don't all have full dates, but they follow a consistent pattern where the year is the last token:
#-- Year 
#-- Month Year
#-- Month Day, Year 
def get_release_year(release_date):
    tokens = release_date.split(' ')
    return tokens[len(tokens)-1]

def update_presence(RPC, data, game_data, start_time, username, achievementData, displayUsername):
    completionAchievement = int((achievementData['NumAwardedToUser'] / achievementData['NumAchievements']) * 100)
    year_of_release = get_release_year(game_data['Released'])
    # details = f"{game_data['GameTitle']} ({year_of_release})"
    largeImageHoverText = f"{achievementData['NumAwardedToUser']} of {achievementData['NumAchievements']} achieved | {completionAchievement} %"
    if(displayUsername):
        largeImageHoverText += f"\nUsername: {username}"
    try:
        RPC.update(
            #state=game_data['GameTitle'],
            details=game_data['Title'],
            state=data['RichPresenceMsg'],
            start=start_time,
            large_image=f"https://media.retroachievements.org{game_data['GameIcon']}",
            # large_text=f"Released {game_data['Released']}, Developed by {game_data['Developer']}, Published by {game_data['Publisher']}",
            large_text = largeImageHoverText,
            small_image=sanitize_console_name(game_data['ConsoleName']),
            small_text=game_data['ConsoleName'],
            # buttons=[{"label": "View RA Profile", "url": f"https://retroachievements.org/user/{username}"}]
        )
    except:
        pass
        

def setup_config():
    config_file = open("config.ini","w")
    print(f'Enter RetroAchievements username: ')
    usr = input()
    print(f'Enter RetroAchievements api_key: ')
    api = input()  

    data = "[DISCORD]\nusername = "+str(usr)+"\napi_key = "+str(api)+"\nclient_id = -1"
    configuring = "\n\n[SETTINGS]\ndisplayUsername = True"

    config_file.write(data + configuring)
    config_file.close()

def main():
    counter = 0
    rpcIsClosed = True
    temp1 = "Nothing1"
    temp2 = 0
    start_time = int(time.time())
    if(os.path.exists('config.ini') == False):
        print(Fore.YELLOW + f"Config file not found. Running first time setup...")
        setup_config()

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    username = config.get('DISCORD', 'username')
    api_key = config.get('DISCORD', 'api_key')
    displayUsername = config.getboolean('SETTINGS', 'displayUsername')

    client_id = config.get('DISCORD', 'client_id') if config.has_option('DISCORD', 'client_id') else "1249693940299333642"
    if(client_id == "-1"):
        client_id = "1249693940299333642"

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    parser.add_argument('--fetch', type=int, default=15, help='Time to sleep before fetches in seconds')
    args = parser.parse_args()

    profile_url = f"https://retroachievements.org/API/API_GetUserProfile.php?u={username}&y={api_key}&z={username}"

    # start_time = int(time.time())

    RPC = Presence(client_id)
    print(Fore.CYAN + "Connecting to Discord App...")
    RPC.connect()
    rpcIsClosed = False
    print(Fore.MAGENTA + "Connected!")

    while True:
        # print(Fore.CYAN + f"Fetching {username}'s RetroAchievements activity...")
        warnings.filterwarnings("ignore")
        data = get_data(profile_url)

        achievement_url = f"https://retroachievements.org/API/API_GetGameInfoAndUserProgress.php?z={username}&y={api_key}&u={username}&g={data['LastGameID']}"

        achievementData = get_data(achievement_url)
        if data is None:
            break

        # print(Fore.MAGENTA + f"Result: {data['RichPresenceMsg']}")

        game_params = f"?z={username}&y={api_key}&i={data['LastGameID']}"
        # print("Last game ID is: ", data['LastGameID'])
        game_url = f"https://retroachievements.org/API/API_GetGame.php{game_params}"
        # print(Fore.CYAN + "Fetching game data...")
        game_data = get_data(game_url)
        if game_data is None:
            break

        # print(Fore.MAGENTA + f"Result: {game_data['GameTitle']}")

        if args.debug:
            print(Fore.YELLOW + "Debug game data:")
            pprint(game_data)
            print("Game data: \n", game_data)
            print("Data: \n", data)

        update_presence(RPC, data, game_data, start_time, username, achievementData, displayUsername)

        # print(Fore.CYAN + f"Sleeping for {args.fetch} seconds...")
        time.sleep(args.fetch)

        # checks if time is up, and nothing between the achievements and status gets changed

        if(temp1 != data['RichPresenceMsg'] or temp2 != achievementData['NumAwardedToUser']):
            counter = 0

        if(counter >= 120 and (temp1 == data['RichPresenceMsg'] or temp2 == achievementData['NumAwardedToUser'])):
            RPC.close()
            rpcIsClosed = True
            counter = 0
        
        
        # checks for no of achievements and status to connect to rcp againn
        if(rpcIsClosed == True and (temp1 != data['RichPresenceMsg'] or temp2 != achievementData['NumAwardedToUser'])):
            RPC.connect()
            rpcIsClosed = False
            start_time = int(time.time())

        # Updates temps and counter
        temp1 = data['RichPresenceMsg']
        temp2 = achievementData['NumAwardedToUser']
        counter += 1


if __name__ == "__main__":
    main()
