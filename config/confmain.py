# Modules

import discord, sys, asyncio, logging, traceback, MySQLdb
from discord.ext.commands import Bot
from discord.ext import commands
from config.secretkeys import botkeydev, botkeymain, mysqlkey
from config.cwd import cwd, cwdmain

# Users with permissions to use dev commands

superusers = ["351211709492363264", # Doc#6431
                   "300285724752609280", # Mitchell#9371
                   "250998121344008193", # Darksniped#0378
                   "201422669889929216", # Nukelar#2781
                   "446047536864690207"] # Philosophy#4859

ranks = ["Private", "Corporal", "Sergeant", "Air Cadet", "Pilot", "Warrant Officer", "MWO", "Flight Lead", "Chief Warrant Officer", "Lieutenant", "Captain", "Major"] 

# Bot Components

def dbconnect():
    if sys.platform == "linux": host = "localhost"
    else: host = "18.218.250.232"
    database = MySQLdb.connect(host=host,port=3306,user='bot',passwd=mysqlkey,db='nato_bot')
    return database, database.cursor()

allowed_channels = [454666331430846476,
                              513845240634015765]

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

# To load the config

def setup(bot): pass