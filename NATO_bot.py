# NATO server bot by Nuk3lar
# This bot will only work on the NATO response command server!
# Discord.py rewrite branch docs https://discord.py.readthedocs.io/en.rewrite/index.html
# Deploy key f5550205ef87d914929c7f67bec8fb866d704761

# Modules

import discord, sys, asyncio, logging, traceback, time, tqdm
from discord.ext.commands import Bot
from discord.ext import commands

# Configs

from config.confmain import cwd, cwdmain, initial_extensions, buildid, Client, bot, mode, botkey, loaded_extentions

# Bot Startup

print('================= NATO bot starting =================')
print(f'[Bot] {mode}')
print(f'[Platform] {sys.platform}\n[CWD] {cwdmain}\n[Build] #{buildid}')
if sys.platform == "linux":
    discord.opus.load_opus(f'{cwdmain}/assets/_bin/libopus.so')
    if discord.opus.is_loaded() == True: print('[Library] Opus Loaded')

# Loading Extensions

if __name__== '__main__':
    print('[ExtensionManager] Loading Extensions')
    logging.info('[ExtensionManager] Loading Extensions')
    succ = 0
    fail = 0
    
    # Extension Loop
    extensions = tqdm.tqdm((initial_extensions), unit=" extensions", ncols=100)
    for extension in extensions:
        extensions.set_description("Loading %s" % extension)
        try:
            bot.load_extension(extension)
            logging.info('[ExtensionManager] Extension: '+extension+' loaded.')
            succ += 1
            extensions.update(len(initial_extensions))
            loaded_extentions.append(extension)
        except Exception as e:
            logging.error('[ExtensionManager] Failed to load extension '+extension+'. ')
            logging.error(f'[ExtensionManager] {extension} {e}')
            fail += 1
            extensions.update(len(initial_extensions))
    print(f'[ExtensionManager] {succ} loaded succsesfuly\n[ExtensionManager] {fail} failed')
    logging.info('[ExtensionManager] Extension Loading Complete')

# Run bot on Discord

bot.run(botkey, bot=True, reconnect=True)