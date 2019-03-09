# Modules

import discord, sys, asyncio, logging, traceback, MySQLdb
from discord.ext.commands import Bot
from discord.ext import commands
from config.secretkeys import botkeydev, botkeymain, mysqlkey
from config.cwd import cwd, cwdmain

# Users with permissions to use dev commands

superusers = ["351211709492363264", # Doc#6431
                   "300285724752609280", # Mitchell#9371
                   "201422669889929216", # Nukelar#2781
                   "446047536864690207"] # Philosophy#4859

ranks = ["Private", "Corporal", "Sergeant", "Air Cadet", "Pilot", "Warrant Officer", "MWO", "Flight Lead", "Chief Warrant Officer", "Lieutenant", "Captain", "Major"] 

# Bot Components

def dbconnect():
    if sys.platform == "linux": host = "localhost"
    else: host = "18.218.250.232"
    database = MySQLdb.connect(host=host,port=3306,user='bot',passwd=mysqlkey,db='nato_bot')
    return database, database.cursor()

allowed_channels = [454666331430846476, 513845240634015765]

def check_channel(id):
    if id in allowed_channels: return True
    else: return False
def perm_check_superuser(id):
    if str(id) in superusers: return True
    else: return False

initial_extensions = ["assets.lib.functions.events",
                             "assets.lib.commands.help",
                             "assets.lib.commands.dev",
                             "assets.lib.commands.fun",
                             "assets.lib.commands.unit"]

# Defining Client & Bot

Client = discord.Client()
bot = commands.Bot(command_prefix = "+")

# Mode Selection

print("======== Mode Selection ========")
print("Defaults to main bot")
print(" 1 | Main bot")
print(" 2 | Development bot")

modeselect = input('Select mode, or press enter to default: ')

if modeselect == "1":
    botkey = botkeymain
    mode = "Main bot"
elif modeselect == "2":
    botkey = botkeydev
    mode = "Development Bot"
elif modeselect == "":
    botkey = botkeymain
    mode = "Main bot"
else:
    botkey = botkeymain
    print("Invalid Entry, defaulting to main bot")
    mode = "Main bot"

# Misc Var Assignments

# Logging config

logging.basicConfig(filename='output.log', filemode='w', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Other random variables

loaded_extentions = []

#   - Build ID
if sys.platform == "linux":
    with open(f"{cwdmain}/buildid.txt", "r") as f:
        buildid=f.read()
        f.close()
if sys.platform == "win32":
    with open(f"{cwdmain}\\buildid.txt", "r") as f:
        buildid=f.read()
        f.close()
#   - Global Embed Colors
embedcolorlight=0x3487C9
embedcolordark=0x00408A
errorcolor=0xb20000

user_dm_message = """, welcome to NATO response unit, we are group of many milsim units that are gathered from around the world.
If you want, you can just stay in the NATO response unit, or you can choose from one of the following groups:
```Dark Owls- a PMC group created and Managed by Dark, they specialize in airborne infiltration, supporting main forces or just joining them in the hells of battlefield. You can expect to be given training and be part of small fireteam in brotherhood fashion.\n
Royal Canadians Dragoons - those are our armoured units in NATO response team. They often fight through the visor of their iron Pegasus, they haven't been active for a while but when they are in action it's good to have them beside you. They are lead by Arakdar.\n
USMC  - one of the most populated group in our unit, they are going on with big explosion in and leaving no one behind, if you been looking for some mediocre unit to join and have fun in masses this is the one to join. they are lead Wolf\n
Lost legion - guys with a lot of fun, commonly fight in groups or join the other in the action. Lead by Mitchell\n
Rangers - Heavy milsim unit which will kick your ass no matter how far you are, expect to be drilled. Otherwise they are fun guys who knows their ways around weapons. Lead by ETA.```
You can find all the link to those units in the channel <#497948185881477160>\n
Promotions are given for attending OP's and having particlar skills/traits\n
We are limiting some equipment, you can see those in <#516768324475027466>\n
We are going to be happy to fight along side you on our next OP which is each Saturday and Sunday at 18:00 GMT
If you have any question, feel free to send a message to on of our Captains or to anyone with a role of Staff.
Wish you luck and good kills."""

# To load the config

def setup(bot): pass