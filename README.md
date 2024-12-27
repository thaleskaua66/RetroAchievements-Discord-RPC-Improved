# RetroAchievements-Discord-Presence-Improved

This is a simple that allows RetroAchievements rich presence to be tracked on discord's rich presence.

## Instructions

1. Install Python. _(It works currently at version 3.13.1)_
2. Run `cmd` and ensure that python is installed correctly by entering this command `py --version`.
3. Run the command, `py -m pip install -r requirements.txt`. Make sure that you're running this command in this directory.
4. Open Discord App. (_NOTE: Discord App should always be opened first before running the `run.bat` file._)
5. Go to Discord > User Settings > Activity Privacy. Toggle on `Share your detected activity with others.`
6. Run the `run.bat` file, enter your credentials, `username` and `api key` from RetroAchievements.

After running the `run.bat` file, a `config.ini` file will be created in the same directory. The credentials that you've submitted are stored in this config file.

### If you want to run the batch file in the background:
1. Run the `batRunner.vbs` file instead of the `run.bat`. _(You can only do this once you've configured your credentials and your rich presence works already.)_ Otherwise, run your `run.bat` file. 
2. Since running the `batRunner.vbs` file makes the process not visible on the taskbar, you need to run the `batStopper.bat` to stop the rich presence from working. _(Otherwise, the other way is to stop `Python` from running on your task manager)_
3. It is also possible to make the `batRunner.vbs` file to run as startup app.<br>
   Make a shortcut of the file > Windows + R > Type `shell:startup`, then press Enter > Place the shortcut in this directory.<br><br>
_Note: This function is still under development and isn't fully functional yet. For some reasons, `bat` files are being terminated when running for a certain period of time without much processes happening._

## Features:
- The game icon is displayed on the Discord's RP.
- The console currently being played is also displayed. 
- Hovering over the game icon displays the user's achievement status about the current game. _(e.g, 32 of 148 achieved | 21 %)_
- A first button that redirects to the user's RA profile. _(Don't worry, I made an option to turn this off)_
- If the username display is turned off, the first button will have the link of the RetroAchievements website instead.
- A second button that redirects to the current game info inside the RetroAchievements website. 
- Not having updates within the current game status for a certain period of time would lead to RP idling. This helps to prevent unintended up-counting of elapsed time. _(Still have occasional issues)_
- Making movements that triggers the game status would display the Discord RP again. _(Still have occasional issues)_
- Optimized game title.
- Optimized game status.

If you want to keep the rich presence running, you can just edit the `config.ini` file and modify the value. By default, it is set to `False`. Turn this to `True` if you want to keep it running without idling.

### How to turn off username display?
1. If ever you don't want your username to have a redirection button on your Discord RP, just edit the `config.ini` file and modify the value inside the `displayUsername` to `False`. By default, this is `True`. _Notice the capital letters in the True and False as wrong cases may result to an error._
2. After this, you can just close the `run.bat` file and open it again to reflect changes. 
