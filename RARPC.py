import argparse
from colorama import Fore, Style, init
import configparser
from datetime import datetime, timezone
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

def getUserProfile(api_key, username):
    data = get_data(f"https://retroachievements.org/API/API_GetUserProfile.php?y={api_key}&u={username}")
    return data

def getUserRecentlyPlayedGame(api_key, username, number_of_results):
    data = get_data(f"https://retroachievements.org/API/API_GetUserRecentlyPlayedGames.php?y={api_key}&u={username}&c={number_of_results}")
    return data[0]

def timeDifferenceFromNow(timeStamp):
    current_time = datetime.now(timezone.utc)
    target_time = datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    differenceInSeconds = abs((target_time - current_time).total_seconds())
    return int(differenceInSeconds)

def minutesToSeconds(minutes):
    return minutes * 60

def isDiscordRunning():
    # Check if discord.exe is in the list of running processes
    for proc in psutil.process_iter(['name']):
        if 'discord.exe' in proc.info['name'].lower():
            print(Fore.GREEN + "Discord is running.")
            return True
    print(Fore.RED + "Discord is not running.")
    return False

def update_presence(RPC, userProfile, recentlyPlayedGame, isDisplayUsername, start_time):
    button1Link = None
    completionPercentage = int((recentlyPlayedGame['NumAchieved'] / recentlyPlayedGame['NumPossibleAchievements']) * 100)
    largeImageHoverText = f"{recentlyPlayedGame['NumAchieved']} of {recentlyPlayedGame['NumPossibleAchievements']} achieved🏆| {completionPercentage} %"
    if(isDisplayUsername):
        button1Link = {"label": "Visit Profile 👤", "url": f"https://retroachievements.org/user/{userProfile['User']}"}
    else:
        button1Link = {"label": "What is RetroAchievements❓", "url": "https://retroachievements.org"}
    
    button2Link = {"label": "Game Info 🎮", "url": f"https://retroachievements.org/game/{recentlyPlayedGame['GameID']}"}
    
    try:
        RPC.update(
            details=recentlyPlayedGame['Title'],
            state=userProfile['RichPresenceMsg'],
            start=start_time,
            large_image=f"https://media.retroachievements.org{recentlyPlayedGame['ImageIcon']}",
            large_text = largeImageHoverText,
            small_image= consoleIcons.get(recentlyPlayedGame['ConsoleID']),
            small_text=recentlyPlayedGame['ConsoleName'],
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
    configuring = "\n\n[SETTINGS]\ndisplayUsername = True\nkeepRunning = False"
    

    config_file.write(data + configuring)
    config_file.close()

def main():
    # GLOBAL SET
    isRPCRunning = False

    print(Fore.YELLOW + "HOW TO USE:\n1. Open Discord app.\n2. Run this script.\nDiscord app should be running first before this script.\n")

    if(os.path.exists('config.ini') == False):
        print(Fore.YELLOW + f"Config file not found. Running first time setup...")
        setup_config()

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    username = config.get('DISCORD', 'username')
    api_key = config.get('DISCORD', 'api_key')
    isDisplayUsername = config.getboolean('SETTINGS', 'displayUsername')
    keepRunning = config.getboolean('SETTINGS', 'keepRunning')

    client_id = "1320752097989234869"

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
        warnings.filterwarnings("ignore")

        # For getting the rich presence message
        userProfile = getUserProfile(api_key, username)

        # For getting the recently played game
        recentlyPlayedGame = getUserRecentlyPlayedGame(api_key, username, 1)

        if(keepRunning == False):
            if(timeDifferenceFromNow(recentlyPlayedGame['LastPlayed']) < minutesToSeconds(1)): # The one here should be edited
                # print("Updating presence...")
                if(isRPCRunning == False):
                    start_time = int(time.time())
                update_presence(RPC, userProfile, recentlyPlayedGame, isDisplayUsername, start_time)
                isRPCRunning = True
            else:
                # print("Presence cleared...")
                RPC.clear()
                isRPCRunning = False
        else:
            update_presence(RPC, userProfile, recentlyPlayedGame, isDisplayUsername, start_time)

        time.sleep(15)
        
if __name__ == "__main__":
    main()
