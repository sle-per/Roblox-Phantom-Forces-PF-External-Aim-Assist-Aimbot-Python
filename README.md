# Phantom Forces Aimbot/Aim Assist
# Contents of File:
1. main.py (main script)
2. trigger.py (modified from main script to include triggerbot; read Functions below)
3. enemyIndic3.png (required by the script, used for recognising enemies flagged by ballistics tracker)
4. lib-check.py (debugging tool that checks if you have the required libraries installed)
Externally coded using python
Libraries Required:
1. OpenCV-python (cv2)
2. MSS
3. numpy
4. pywin32
# Functions:
Aimbot
Triggerbot (Will interfere with your firing inputs, therefore is separated from main.py as trigger.py)
# Requires Ballistics Tracker attachment on the weapon
# Also requires modification to script by plain text (open main.py/ trigger.py with text editing apps like Notepad)
# How to use script:
1. Download the entire file in zip and extract to wherever you like
2. Run *lib-check.py* to ensure that you have installed the required libraries (script won't work if you don't install them)
3. Open *main.py* or *trigger.py* with Notepad or any text editing software
4. Scroll or use Find Tool to find the phrase *Sensitivity*
5. Input the corresponding sensitivity values for each setting
6. Save the changes
7. Open up *enemyIndic3* and check that it is a cropped image of the ballistics tracker indicator
8. Open up python IDLE and load the script (File ->Open file ->main.py/trigger.py)
9. Run the script and leave the 2nd IDLE window open
10. Play the game and enjoy the advantages of python
# NOTE: trigger.py contains all the featurs from main.py, so there is no need to run both at the same time.
