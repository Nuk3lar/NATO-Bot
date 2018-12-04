# Modules

import discord, sys, asyncio, logging, traceback, os, sys, aiohttp
from discord.ext.commands import Bot
from discord.ext import commands
from config.confmain import Client, bot, embedcolordark, embedcolorlight, buildid, cwd, cwdmain

# Changing the Status Message

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Activity(name='+help', type=0))
        await asyncio.sleep(20)
        await bot.change_presence(activity=discord.Activity(name="ARMA", type=0))
        users = 0
        guild = bot.get_guild(455355408719151104)
        await asyncio.sleep(20)
        await bot.change_presence(activity=discord.Activity(name=f'with {len(guild.members)} soilders', type=0))
        await asyncio.sleep(20)
        


async def update_roles_task():
        guild = bot.get_guild(455355408719151104)
        from config.confmain import ranks
        while True:
            
            users_1 = {}
            for user in guild.members:
                for role in user.roles:
                    if role.name in ranks: 
                        users_1[str(user.id)] = role.name
                        break
                    else: users_1[str(user.id)] = None
            from config.confmain import dbconnect
            db = dbconnect()
            from assets.lib.functions.database import get_ranks, update_user_rank
            users_2 = get_ranks(db)
            update = 0
            for user in guild.members:
                if users_2[str(user.id)] != users_1[str(user.id)]:
                    update_user_rank(db, user, users_1[str(user.id)])
                    update += 1
            if update > 0: logging.info(f"[USERS] {update} user(s) db rank updated") 
            db[0].commit()
            db[0].close()
            await asyncio.sleep(600)
# When Bot is Connected and ready

class on_ready:
    # Setup INIT
    def __init__(self, bot): self.bot = bot
    def __unload(self): pass
    @Client.event
    async def on_ready(self):
        print(f'[Bot user] {bot.user.name}\n[Bot ID] {bot.user.id}')
        logging.info("NATO-Bot #"+buildid+" STARTED")
        bot.loop.create_task(status_task())
        bot.loop.create_task(update_roles_task())
        print(f'============== NATO-Bot build #{buildid} Started ==============')

class on_join:
    def __init__(self, bot): self.bot = bot
    def __unload(self): pass
    @Client.event
    async def on_member_join(self, member):
        channel = bot.get_channel(455355408719151106)
        await channel.send(f"{member.mention} Welcome to NRC!\nPlease check <#518000366856699915> for the rules and\n<#455359684761878528> for the current modpack.")
        from config.confmain import dbconnect
        db = dbconnect()
        logging.info(f"[USERS] {member.id} Joined server")
        from assets.lib.functions.database import add_user, get_users
        if not(str(member.id) in get_users(db)): add_user(db, member, rank=None)
        db[0].commit()
        db[0].close()
        


# For Loading Module

def setup(bot):
    bot.add_cog(on_ready(bot))
    bot.add_cog(on_join(bot))