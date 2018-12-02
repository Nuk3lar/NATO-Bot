# Modules

import discord, sys, asyncio, logging, traceback
from discord.ext.commands import Bot
from discord.ext import commands
from config.confmain import cwd, cwdmain, embedcolordark, embedcolorlight, errorcolor, check_channel

# Switch function for help command

# Embed returns
class help_switch_class():
    @staticmethod
    def none():
        embed=discord.Embed(title="Help for NATO Server Bot", description="[FILLER]", color=embedcolordark)
        return embed
# Cases
help_switch_cases = {
    None : help_switch_class.none
    }
# Function
def switch( ch, help_switch_cases, self, *args):
    try: len(*args)
    except TypeError: return help_switch_cases[ ch ]( )
    return help_switch_cases[ ch ]( self, *args )

# Help Command

class HelpCMD:
    def __init__(self, bot): self.bot = bot
    @commands.command(name='help')
    async def _help(self, message, *, part : str = None):
        while True:
            if check_channel(message.channel.id) == False:
                    logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                    msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                    time.sleep(3)
                    await msg_wrong_channel.delete()
                    await message.message.delete()
                    break
            logging.info(f"User {message.author.id} ran command Help with parameters: {part}")
            parts = ["help"]
            if (part in parts): await message.channel.send("", embed=switch(part, help_switch_cases, self, part))
            elif part == None: await message.channel.send("", embed=switch(None, help_switch_cases, self))
            break

# For Loading Module

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCMD(bot))