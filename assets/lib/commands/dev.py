# Modules

import discord, sys, asyncio, logging, traceback, time, os
from discord.ext.commands import Bot
from discord.ext import commands
from shutil import copyfile
from config.confmain import cwd, cwdmain, embedcolordark, embedcolorlight, errorcolor, superusers, check_channel, Client, initial_extensions, bot

# Check Functions

def perm_check_superuser(id):
    if str(id) in superusers: return True
    else: return False

# Purge Commands

class purge:
    def __init__(self, bot): self.bot = bot
    def __unload(self): pass
    
    @commands.command(name="purge")
    async def _purge(self, message, *, to_purge : int = 1):
        while True:
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command shutdown and was denied!")
                msg_no_perms = await message.channel.send("You can't do that Command!")
                time.sleep(3)
                await msg_no_perms.delete()
                await message.message.delete()
                break
            logging.info(f"User {message.author.id} ran command purge")
            msg_to_delete = []
            async for msg in message.channel.history(limit = to_purge): msg_to_delete.append(msg)
            if to_purge < 1:
                msg_bad_num = await message.channel.send("Negative numbers dont work БЛЯДЬ")
                time.sleep(3)
                await msg_bad_num.delete()
                break
            if to_purge > 100:
                for msg_num in range(len(msg_to_delete)): await msg_to_delete[msg_num].delete()
            else: 
                try: await message.channel.delete_messages(msg_to_delete)
                except: 
                    for msg_num in range(len(msg_to_delete)): await msg_to_delete[msg_num].delete()
            if to_purge == 1: succ_msg = await message.channel.send("", embed=discord.Embed(title=u'\u2705 Purged '+str(to_purge)+' message!', color=errorcolor))
            else: succ_msg = await message.channel.send("", embed=discord.Embed(title=u'\u2705 Purged '+str(to_purge)+' messages!', color=errorcolor))
            time.sleep(5)
            await succ_msg.delete()
            break
            


# Stop/Restart

class stopstart:
    def __init__(self, bot): self.bot = bot
    def __unload(self): pass
    # Shutdown Command Block
    @commands.command(name='shutdown')
    async def _stop(self, message):
        while True:
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command shutdown and was denied!")
                msg_no_perms = await message.channel.send("You can't do that Command!")
                time.sleep(3)
                await msg_no_perms.delete()
                await message.message.delete()
                break
            if check_channel(message.channel.id) == False:
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await msg_wrong_channel.delete()
                await message.message.delete()
                break
            logging.info(f"User {message.author.id} ran command shutdown")
            botmsg = await message.channel.send("", embed=discord.Embed(title='Bot will shutdown', color=errorcolor))
            time.sleep(2)
            if sys.platform == "win32": cfg = [f"{cwdmain}\\logs\\output.cfg", "logs\\"]
            else: cfg = [f"{cwdmain}/logs/output.cfg", f"{cwdmain}/logs/"]
            open_cfg = open(cfg[0], "r")
            outputcount = int(open_cfg.read())
            open_cfg.close()
            outputcount += 1
            write_cfg = open(cfg[0], "w+")
            write_cfg.write(str(outputcount))
            write_cfg.close()
            await botmsg.edit(embed=discord.Embed(title="Saving logs...", color=errorcolor))
            copyfile('output.log', f"{cfg[1]}log_{outputcount}.log")
            await botmsg.edit(embed=discord.Embed(title="Done, killing processes", color=errorcolor))
            await Client.close()
            logging.info("BOT SHUTTING DOWN")
            if sys.platform == "win32": os.system('taskkill /f /im python.exe')
            else: os.system('killall -9 python3.6')
            break
    # Restart Command Block
    @commands.command(name="restart")
    async def _restart(self, message):
        while True:
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command restart and was denied!")
                msg_no_perms = await message.channel.send("You can't do that Command!")
                time.sleep(3)
                await msg_no_perms.delete()
                await message.message.delete()
                break
            if check_channel(message.channel.id) == False:
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await msg_wrong_channel.delete()
                await message.message.delete()
                break
            logging.info(f"User {message.author.id} ran command restart")
            restartembed=discord.Embed(title="Bot Restarting", color=errorcolor)
            botmsg = await message.channel.send("", embed=restartembed)
            logging.info("Reloading all plugins")
            succ = 0
            fail = 0
            for extension in initial_extensions:
                self.bot.unload_extension(extension)
                restartembed.add_field(name=extension, value='Unloaded.')
                try:
                    self.bot.load_extension(extension)
                    restartembed.add_field(name=f'{extension}', value='Reloaded.', inline=False)
                    await botmsg.edit(embed=restartembed)
                    succ += 1
                except Exception as e:
                    restartembed.add_field(name=f'{extension}', value='Failed to reload!', inline=False)
                    await botmsg.edit(embed=restartembed)
                    logging.error('[ExtensionManager] Failed to load extension '+extension+'. ')
                    logging.error(f'[ExtensionManager] {extension} {e}')
                    fail += 1
            logging.info(f"Done reloading plugins {fail} failed to load")
            restartembed.add_field(name="Finished reloading extensions", value=f"{succ} Loaded Succsesfully\n{fail} Failed to load in")
            await botmsg.edit(embed=restartembed)
            time.sleep(1)
            if sys.platform == "win32": cfg = [f"{cwdmain}\\logs\\output.cfg", "logs\\"]
            else: cfg = [f"{cwdmain}/logs/output.cfg", f"{cwdmain}/logs/"]
            open_cfg = open(cfg[0], "r")
            outputcount = int(open_cfg.read())
            open_cfg.close()
            outputcount += 1
            write_cfg = open(cfg[0], "w+")
            write_cfg.write(str(outputcount))
            write_cfg.close()
            await botmsg.edit(embed=discord.Embed(title="Saving logs...", color=errorcolor))
            copyfile('output.log', f"{cfg[1]}log_{outputcount}.log")
            await botmsg.edit(embed=discord.Embed(title=u'\u2705 Done!', color=errorcolor))
            logging.info("Restart Done")
            break
            
# Load/Unload

class load_unload:
    def __init__(self, bot): self.bot = bot
    def __unload(self): pass
    # Load command block
    @commands.command(name="load")
    async def _load(self, message, *, part : str = None):
        while True:
            if part == None: break
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command load and was denied!")
                msg_no_perms = await message.channel.send("You can't do that Command!")
                time.sleep(3)
                await msg_no_perms.delete()
                await message.message.delete()
                break
            if check_channel(message.channel.id) == False:
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await msg_wrong_channel.delete()
                await message.message.delete()
                break
            from config.confmain import loaded_extentions
            if "assets.lib."+part in loaded_extentions: 
                await message.channel.send("", embed=discord.Embed(title=u"\u274C That is already loaded!", color=errorcolor))
                logging.info(f'User {message.author.id} tried to load extension: assets.lib.{part}, but it was already loaded!')
                break
            logging.info(f"User {message.author.id} ran command load")
            logging.info(f'[ExtensionManager] Attempting to load extension: assets.lib.{part}')
            botmsg = await message.channel.send("", embed=discord.Embed(title=f"Loading assets.lib.{part}", color=errorcolor))
            try:
                self.bot.load_extension(f"assets.lib.{part}")
                loaded_extentions.append("assets.lib."+part)
                await botmsg.edit(embed=discord.Embed(title=u'\u2705 Loaded Succsessfully', color=errorcolor))
                logging.info(f'[ExtensionManager] Sucsessfuly loaded extension: assets.lib.{part}')
            except Exception as e:
                logging.error('[ExtensionManager] Failed to load extension '+part+'. ')
                logging.error(f'[ExtensionManager] {"assets.lib."+part} {e}')
                if "No module named" in str(e): await botmsg.edit(embed=discord.Embed(title=u"\u274C That is not a module!", color=errorcolor))
                else: await botmsg.edit(embed=discord.Embed(title=u"\u274C Failed to load!", color=errorcolor))
            break
    # Unload command block
    @commands.command(name="unload")
    async def _unload(self, message, *, part : str = None):
        while True:
            if part == None: break
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command restart and was denied!")
                msg_no_perms = await message.channel.send("You can't do that Command!")
                time.sleep(3)
                await msg_no_perms.delete()
                await message.message.delete()
                break
            if check_channel(message.channel.id) == False:
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await msg_wrong_channel.delete()
                await message.message.delete()
                break
            from config.confmain import loaded_extentions
            if not("assets.lib."+part in loaded_extentions): 
                await message.channel.send("", embed=discord.Embed(title=u"\u274C That is not loaded!", color=errorcolor))
                logging.info(f'User {message.author.id} tried to unload extension: assets.lib.{part}, but it was not loaded!')
                break
            

            logging.info(f"User {message.author.id} ran command unload")
            logging.info(f'[ExtensionManager] Unloading extension: assets.lib.{part}')
            self.bot.unload_extension(f"assets.lib.{part}")
            loaded_extentions.remove(f"assets.lib.{part}")
            botmsg = await message.channel.send("", embed=discord.Embed(title=f"Unloading assets.lib.{part}", color=errorcolor))
            await botmsg.edit(embed=discord.Embed(title=u'\u2705 Unloaded Succsessfully', color=errorcolor))
            logging.info(f'[ExtensionManager] Sucsessfuly unloaded extension: assets.lib.{part}')
            break

    # Reload command block
    @commands.command(name="reload")
    async def _reload(self, message, *, part : str = None):
        while True:
            if part == None: break
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command reload and was denied!")
                msg_no_perms = await message.channel.send("You can't do that Command!")
                time.sleep(3)
                await msg_no_perms.delete()
                await message.message.delete()
                break
            if check_channel(message.channel.id) == False:
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await msg_wrong_channel.delete()
                await message.message.delete()
                break
            from config.confmain import loaded_extentions
            if not("assets.lib."+part) in loaded_extentions: 
                await message.channel.send("", embed=discord.Embed(title=u"\u274C That is not a loaded module!", color=errorcolor))
                logging.info(f'User {message.author.id} tried to reload extension: assets.lib.{part}, but it was not loaded!')
                break
            logging.info(f"User {message.author.id} ran command reload")
            logging.info(f'[ExtensionManager] Attempting to reload extension: assets.lib.{part}')
            logging.info(f'[ExtensionManager] Unloading extension: assets.lib.{part}')
            botmsg = await message.channel.send("", embed=discord.Embed(title=f"Reloading assets.lib.{part}", color=errorcolor))
            self.bot.unload_extension(f"assets.lib.{part}")
            await botmsg.edit(embed=discord.Embed(title=u'\u2705 Unloaded Succsessfully', color=errorcolor))
            loaded_extentions.remove(f"assets.lib.{part}")
            await botmsg.edit(embed=discord.Embed(title=f"Loading assets.lib.{part}", color=errorcolor))
            try:
                self.bot.load_extension(f"assets.lib.{part}")
                loaded_extentions.append("assets.lib."+part)
                await botmsg.edit(embed=discord.Embed(title=u'\u2705 Reloaded Succsessfully', color=errorcolor))
                logging.info(f'[ExtensionManager] Sucsessfuly reloaded extension: assets.lib.{part}')
            except Exception as e:
                logging.error('[ExtensionManager] Failed to load extension '+part+'. ')
                logging.error(f'[ExtensionManager] {"assets.lib."+part} {e}')
                await botmsg.edit(embed=discord.Embed(title=u"\u274C Failed to load back in!", color=errorcolor))
            break

# Misc Commands

class misc_dev:
    def __init__(self, bot): self.bot = bot
    def __unload(self): pass

    # Show loaded modules
    @commands.command(name="loaded")
    async def _loaded(self, message):
        while True:
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command reload and was denied!")
                msg_no_perms = await message.channel.send("You can't do that Command!")
                time.sleep(3)
                await msg_no_perms.delete()
                await message.message.delete()
                break
            if check_channel(message.channel.id) == False:
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await msg_wrong_channel.delete()
                await message.message.delete()
                break
            from config.confmain import loaded_extentions
            embed=discord.Embed(title="Currently Loaded Extentions", color=errorcolor)
            if len(loaded_extentions) == 0: embed.add_field(name=u"\u274C", value="No Modules loaded", inline=False)
            else:
                for extension in loaded_extentions:
                    embed.add_field(name=extension, value="Loaded", inline=False)
            await message.channel.send("", embed=embed) 
            break
# For Loading Modules

def setup(bot):
    bot.add_cog(stopstart(bot))
    bot.add_cog(load_unload(bot))
    bot.add_cog(misc_dev(bot))
    bot.add_cog(purge(bot))