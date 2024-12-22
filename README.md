# RetroAchievements-Discord-Presence

This is a simple that allows RetroAchievements rich presence to be tracked on discord's rich presence.

## Requirements

- Python3
- You can install dependencies with
    ```
    pip install -r requirements.txt
    ```
    - `requests` (https://pypi.org/project/requests/)
    - `pypresence` (https://pypi.org/project/pypresence/)
    - `colorama` (https://pypi.org/project/colorama/)
    - `configparser` (https://pypi.org/project/configparser/)

### Optional
- Discord Application (https://discord.com/developers/applications/) [For the Discord Application ID]

## Running the script / Instructions:

1. Use the included `run.bat` file.
2. During the first run, it will ask for your *Username* and *API KEY* (Both from RetroAchievements).
3. After running the `run.bat` file, a `config.ini` file will be created in the same directory. 
4. The credentials that you've submitted are stored in this config file. 
5. Just use the `config.ini` file when modifying either of these credentials. 

<hr>

## What's New? 
- The game icon is now displayed on the Discord's RP.
- Hovering over the game icon now displays the user's achievement status about the current game. _(e.g, 32 of 148 achievements | 21 %)_
- The username is now also displayed below the current achievement status. Both of these could be seen by hovering on the game icon on Discord RP. _(Don't worry, I made an option to turn this off)_
- Not having movements within the current game status for a certain period of time would lead to RP idling. This helps to prevent unintended up-counting of elapsed time.
- Making movements that triggers the game status would display the Discord RP again.
- Optimized game title.
- Optimized game status.

### How to turn off username display?
1. If ever you don't want your username to be displayed on your RP, just edit the `config.ini` file and modify the value inside the `displayUsername` to `False`. By default, this is `True`. _Notice the capital letters in the True and False as wrong cases may result to an error._
2. After this, you can just close the `run.bat` file and open it again for the changes to reflect. 
