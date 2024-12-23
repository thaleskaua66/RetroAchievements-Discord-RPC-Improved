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

consoleIcons = {
    1: "https://static.retroachievements.org/assets/images/system/md.png",
    2: "https://static.retroachievements.org/assets/images/system/n64.png",
    3: "https://static.retroachievements.org/assets/images/system/snes.png",
    4: "https://static.retroachievements.org/assets/images/system/gb.png",
    5: "https://static.retroachievements.org/assets/images/system/gba.png",
    6: "https://static.retroachievements.org/assets/images/system/gbc.png",
    7: "https://static.retroachievements.org/assets/images/system/nes.png",
    8: "https://static.retroachievements.org/assets/images/system/pce.png",
    9: "https://static.retroachievements.org/assets/images/system/scd.png",
    10: "https://static.retroachievements.org/assets/images/system/32x.png",
    11: "https://static.retroachievements.org/assets/images/system/sms.png",
    12: "https://static.retroachievements.org/assets/images/system/ps1.png",
    13: "https://static.retroachievements.org/assets/images/system/lynx.png",
    14: "https://static.retroachievements.org/assets/images/system/ngp.png",
    15: "https://static.retroachievements.org/assets/images/system/gg.png",
    16: "https://static.retroachievements.org/assets/images/system/gc.png",
    17: "https://static.retroachievements.org/assets/images/system/jag.png",
    18: "https://static.retroachievements.org/assets/images/system/ds.png",
    19: "https://static.retroachievements.org/assets/images/system/wii.png",
    20: "https://static.retroachievements.org/assets/images/system/wiiu.png",
    21: "https://static.retroachievements.org/assets/images/system/ps2.png",
    22: "https://static.retroachievements.org/assets/images/system/xbox.png",
    23: "https://static.retroachievements.org/assets/images/system/mo2.png",
    24: "https://static.retroachievements.org/assets/images/system/mini.png",
    25: "https://static.retroachievements.org/assets/images/system/2600.png",
    26: "https://static.retroachievements.org/assets/images/system/dos.png",
    27: "https://static.retroachievements.org/assets/images/system/arc.png",
    28: "https://static.retroachievements.org/assets/images/system/vb.png",
    29: "https://static.retroachievements.org/assets/images/system/msx.png",
    30: "https://static.retroachievements.org/assets/images/system/c64.png",
    31: "https://static.retroachievements.org/assets/images/system/zx81.png",
    32: "https://static.retroachievements.org/assets/images/system/oric.png",
    33: "https://static.retroachievements.org/assets/images/system/sg1k.png",
    34: "https://static.retroachievements.org/assets/images/system/vic-20.png",
    35: "https://static.retroachievements.org/assets/images/system/amiga.png",
    36: "https://static.retroachievements.org/assets/images/system/ast.png",
    37: "https://static.retroachievements.org/assets/images/system/cpc.png",
    38: "https://static.retroachievements.org/assets/images/system/a2.png",
    39: "https://static.retroachievements.org/assets/images/system/sat.png",
    40: "https://static.retroachievements.org/assets/images/system/dc.png",
    41: "https://static.retroachievements.org/assets/images/system/psp.png",
    42: "https://static.retroachievements.org/assets/images/system/cd-i.png",
    43: "https://static.retroachievements.org/assets/images/system/3do.png",
    44: "https://static.retroachievements.org/assets/images/system/cv.png",
    45: "https://static.retroachievements.org/assets/images/system/intv.png",
    46: "https://static.retroachievements.org/assets/images/system/vect.png",
    47: "https://static.retroachievements.org/assets/images/system/8088.png",
    48: "https://static.retroachievements.org/assets/images/system/9800.png",
    49: "https://static.retroachievements.org/assets/images/system/pc-fx.png",
    50: "https://static.retroachievements.org/assets/images/system/5200.png",
    51: "https://static.retroachievements.org/assets/images/system/7800.png",
    52: "https://static.retroachievements.org/assets/images/system/x68k.png",
    53: "https://static.retroachievements.org/assets/images/system/ws.png",
    54: "https://static.retroachievements.org/assets/images/system/ecv.png",
    55: "https://static.retroachievements.org/assets/images/system/escv.png",
    56: "https://static.retroachievements.org/assets/images/system/ngcd.png",
    57: "https://static.retroachievements.org/assets/images/system/chf.png",
    58: "https://static.retroachievements.org/assets/images/system/fm-towns.png",
    59: "https://static.retroachievements.org/assets/images/system/zxs.png",
    60: "https://static.retroachievements.org/assets/images/system/g&w.png",
    61: "https://static.retroachievements.org/assets/images/system/n-gage.png",
    62: "https://static.retroachievements.org/assets/images/system/3ds.png",
    63: "https://static.retroachievements.org/assets/images/system/wsv.png",
    64: "https://static.retroachievements.org/assets/images/system/x1.png",
    65: "https://static.retroachievements.org/assets/images/system/tic-80.png",
    66: "https://static.retroachievements.org/assets/images/system/to8.png",
    67: "https://static.retroachievements.org/assets/images/system/pc-6000.png",
    68: "https://static.retroachievements.org/assets/images/system/pico.png",
    69: "https://static.retroachievements.org/assets/images/system/duck.png",
    70: "https://static.retroachievements.org/assets/images/system/zeebo.png",
    71: "https://static.retroachievements.org/assets/images/system/ard.png",
    72: "https://static.retroachievements.org/assets/images/system/wasm4.png",
    73: "https://static.retroachievements.org/assets/images/system/a2001.png",
    74: "https://static.retroachievements.org/assets/images/system/vc4000.png",
    75: "https://static.retroachievements.org/assets/images/system/elek.png",
    76: "https://static.retroachievements.org/assets/images/system/pccd.png",
    77: "https://static.retroachievements.org/assets/images/system/jcd.png",
    78: "https://static.retroachievements.org/assets/images/system/dsi.png",
    79: "https://static.retroachievements.org/assets/images/system/ti-83.png",
    80: "https://static.retroachievements.org/assets/images/system/uze.png",
    81: "https://static.retroachievements.org/assets/images/system/fds.png",
    100: "https://static.retroachievements.org/assets/images/system/hubs.png",
    101: "https://static.retroachievements.org/assets/images/system/events.png",
    102: "https://static.retroachievements.org/assets/images/system/exe.png"
}

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
            small_image= consoleIcons.get(game_data['ConsoleID']),
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

    client_id = "1320752097989234869"

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
