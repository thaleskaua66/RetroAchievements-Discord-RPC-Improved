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
from allSystems import consoleIcons
import psutil

global counter
global RPC
global rpcIsOpen
global temp1, temp2
global start_time
global countLimit

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

def isDiscordRunning():
    # Check if discord.exe is in the list of running processes
    for proc in psutil.process_iter(['name']):
        if 'discord.exe' in proc.info['name'].lower():
            print(Fore.GREEN + "Discord is running.")
            return True
    print(Fore.RED + "Discord is not running.")
    return False

def update_presence(RPC, data, game_data, start_time, username, achievementData, displayUsername, lastGameID):
    button1Link = None
    completionAchievement = int((achievementData['NumAwardedToUser'] / achievementData['NumAchievements']) * 100)
    largeImageHoverText = f"{achievementData['NumAwardedToUser']} of {achievementData['NumAchievements']} achieved🏆| {completionAchievement} %"
    if(displayUsername):
        button1Link = {"label": "Visit Profile 👤", "url": f"https://retroachievements.org/user/{username}"}
    else:
        button1Link = {"label": "What is RetroAchievements❓", "url": "https://retroachievements.org"}
    
    button2Link = {"label": "Game Info 🎮", "url": f"https://retroachievements.org/game/{lastGameID}"}
    
    try:
        RPC.update(
            #state=game_data['GameTitle'],
            details=game_data['Title'],
            state=data['RichPresenceMsg'],
            start=start_time,
            large_image=f"https://media.retroachievements.org{game_data['GameIcon']}",
            # large_text=f"Released {game_data['Released']}, Developed by {game_data['Developer']}, Published by {game_data['Publisher']}",
            large_text = largeImageHoverText,
            small_image= consoleIcons.get(game_data['ConsoleID']),
            small_text=game_data['ConsoleName'],
            buttons=[button1Link, button2Link]
        )
    except:
        print(Fore.RED + "Failed to update presence.")
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
    # Global variables SET
    counter = 120
    rpcIsOpen = False
    temp1 = None
    temp2 = None
    countLimit = 120

    print(Fore.YELLOW + "HOW TO USE:\n1. Open Discord app.\n2. Run this script.\nDiscord app should be running first before this script.\n")

    if(os.path.exists('config.ini') == False):
        print(Fore.YELLOW + f"Config file not found. Running first time setup...")
        setup_config()

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    username = config.get('DISCORD', 'username')
    api_key = config.get('DISCORD', 'api_key')
    displayUsername = config.getboolean('SETTINGS', 'displayUsername')

    client_id = "1320752097989234869"

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    parser.add_argument('--fetch', type=int, default=15, help='Time to sleep before fetches in seconds')
    args = parser.parse_args()

    profile_url = f"https://retroachievements.org/API/API_GetUserProfile.php?u={username}&y={api_key}&z={username}"


    RPC = Presence(client_id)
    print(Fore.CYAN + "Connecting to Discord App...")

    while(isDiscordRunning() == False):
        print(Fore.RED + "Retrying in 10 seconds...")
        time.sleep(10)

    time.sleep(5)
    RPC.connect()

    print(Fore.MAGENTA + "Connected!")
    start_time = int(time.time())

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

        # Checks whether to show the presence or clear it
        if(rpcIsOpen == True and (temp1 != data['RichPresenceMsg'] or temp2 != achievementData['NumAwardedToUser'])):
            # print("Enters condition 1: RPC is open and data has changed")
            update_presence(RPC, data, game_data, start_time, username, achievementData, displayUsername, data['LastGameID'])
            counter = 1

        if(rpcIsOpen == False and (temp1 != data['RichPresenceMsg'] or temp2 != achievementData['NumAwardedToUser'])):
            # print("Enters condition 2: RPC is closed and data has changed. RPC now turns on.")
            start_time = int(time.time())
            update_presence(RPC, data, game_data, start_time, username, achievementData, displayUsername, data['LastGameID'])
            counter = 1
            rpcIsOpen = True
        elif(rpcIsOpen == True and counter >= countLimit and (temp1 == data['RichPresenceMsg'] or temp2 == achievementData['NumAwardedToUser'])):
            # print("Enters condition 3: RPC is open and data has not changed for a certain time period. RPC now turns off.")
            RPC.clear()
            rpcIsOpen = False

        # print("At this point, counter is now: ", counter)
            
        temp1 = data['RichPresenceMsg']
        temp2 = achievementData['NumAwardedToUser']
        counter += 1

        time.sleep(args.fetch)
        
if __name__ == "__main__":
    main()
