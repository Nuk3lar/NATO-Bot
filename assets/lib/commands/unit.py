# Modules

import discord, sys, asyncio, logging, traceback, time, os, validators
from discord.ext.commands import Bot
from discord.ext import commands
from config.confmain import cwd, cwdmain, embedcolordark, embedcolorlight, errorcolor, check_channel, Client, ranks, perm_check_superuser, bot

# Database linked command to check individual member's MOS Training.
class information_database_command:
    def __init__(self, bot): self.bot = bot
    def __unload(self): pass

    # Information Database Command
    @commands.command(name="info")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _info(self, message, *, target: discord.Member = None):
        while True:
            if check_channel(message.channel.id) == False: # Lines 16-22 are Check Func
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await message_wrong_channel.delete()
                await message.message.delete()
                break
            if target == None: target = message.author
            from config.confmain import dbconnect
            db = dbconnect()
            from assets.lib.functions.database import get_user
            userdb = get_user(db, target)
            for field_enum in range(len(userdb)):
                if userdb[field_enum] == None: userdb[field_enum] = ("Not Set")
            if userdb[2] == "Not Set": userdb[2] = "Unranked"
            if userdb[7] == "Not Set": userdb[7] = None
            url_embed = f"https://raw.githubusercontent.com/Nuk3lar/miscassets/master/ranks/{userdb[2].replace(' ', '%20')}.png"
            information_embed = discord.Embed(title=f"Information On Soldier: {target.name}", description="", color=embedcolorlight)
            information_embed.set_author(name=target.name, icon_url=target.avatar_url)
            information_embed.set_thumbnail(url=url_embed)
            information_embed.add_field(name=f"Rank", value=userdb[2], inline = True)
            information_embed.add_field(name=f"MOS", value=userdb[3], inline = True)
            information_embed.add_field(name=f"Callsign", value=userdb[4], inline = True)
            information_embed.add_field(name=f"Status", value=userdb[5], inline = True)
            if not(userdb[7] == None): information_embed.set_footer(text=userdb[7])
            await message.channel.send("", embed=information_embed)
            break

    @_info.error
    async def _info_error(self, message, error):
        if isinstance(error, commands.CommandOnCooldown): await message.channel.send(f"Command on cooldown! Try again in {round(error.retry_after, 1)}s")



    @commands.command(name="test_")
    async def _test_(self, message):
        roles = {}
        for role in range(len(message.guild.roles)):  roles[message.guild.roles[role].name] = message.guild.roles[role].id
        print(roles)
    @commands.command(name="adduser")
    async def _adduser(self, message):
        while True:
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command reload and was denied!")
                msg_no_perms = await message.channel.send("Restricted!")
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
            users = {}
            for user in message.guild.members:
                for role in user.roles:
                    if role.name in ranks: 
                        users[str(user.id)] = role.name
                        break
                    else: users[str(user.id)] = None
            from config.confmain import dbconnect
            db = dbconnect()
            from assets.lib.functions.database import get_users, add_user
            db_ids = get_users(db)
            if len(db_ids) == len(message.guild.members): await message.channel.send("", embed=discord.Embed(title=u"\u274C No need!", color=errorcolor))
            else:    
                add = 0
                for user in message.guild.members:
                    if str(user.id) in db_ids: pass
                    else: 
                        add_user(db, user, users[str(user.id)])
                        add += 1
                await message.channel.send("", embed=discord.Embed(title=u"\u2705 Added "+str(add)+" user(s) not in DB!", color=errorcolor))
            db[0].commit()
            db[0].close()
            

            #def getranked(users, rank_find):
            #    ranked = []
            #    list_items = users.items()
            #    for item  in list_items:
            #        if item[1] == rank_find: ranked.append(item[0])
            #    return ranked
            #for rank in ranks: print(getranked(users, rank))
            break


    #mos Setting Command
    @commands.command(name="mos")
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _mos(self, message, *, mos : str = None):
        while True: 
            if check_channel(message.channel.id) == False: # Lines 17-23 are Check Func
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await message_wrong_channel.delete()
                await message.message.delete()
                break
            if mos == None:
                await message.channel.send("", embed=discord.Embed(title=":x: Please fill out your MOS with:", description="Medic, AT/AA, LMG etc.", color=errorcolor))
                message.command.reset_cooldown(message)
                break
            from config.confmain import dbconnect
            db = dbconnect()
            from assets.lib.functions.database import set_mos
            set_mos(db, message.author, mos)
            db[0].commit()
            db[0].close()
            await message.channel.send("", embed=discord.Embed(title=f":white_check_mark: Your MOS has been set to: {mos}", color=embedcolorlight))
            break

    @_mos.error
    async def _mos_error(self, message, error):
        if isinstance(error, commands.CommandOnCooldown): await message.channel.send(f"Command on cooldown! Try again in {round(error.retry_after, 1)}s")


     #desc Setting Command
    @commands.command(name="desc")
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _descr(self, message, *, descr : str = None):
        while True: 
            if check_channel(message.channel.id) == False: # Lines 17-23 are Check Func
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await message_wrong_channel.delete()
                await message.message.delete()
                break
            if descr == None:
                await message.channel.send("", embed=discord.Embed(title=":x: Please fill out your description", color=errorcolor))
                message.command.reset_cooldown(message)
                break
            from config.confmain import dbconnect
            db = dbconnect()
            from assets.lib.functions.database import set_descr
            set_descr(db, message.author, descr)
            db[0].commit()
            db[0].close()
            await message.channel.send("", embed=discord.Embed(title=f":white_check_mark: Your Description has been set to: {descr}", color=embedcolorlight))
            break

    @_descr.error
    async def _descr_error(self, message, error):
        if isinstance(error, commands.CommandOnCooldown): await message.channel.send(f"Command on cooldown! Try again in {round(error.retry_after, 1)}s")
            


    @commands.command(name="callsign")
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _callsign(self, message, *, callsign : str = None):
        while True:
            if check_channel(message.channel.id) == False: # Lines 17-23 are Check Func
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await message_wrong_channel.delete()
                await message.message.delete()
                break
            from config.confmain import dbconnect
            db = dbconnect()
            from assets.lib.functions.database import set_callsign
            if not(callsign == None):
                set_callsign(db, message.author, callsign)
                await message.channel.send("", embed=discord.Embed(title=u'\u2705 Callsign set to: '+callsign, color=embedcolordark))
                db[0].commit()
                db[0].close()
                break
            embed=discord.Embed(title="Set embed", description="Reply (within 10 secs) to set a callsign for +info",  color = embedcolordark)
            embed.add_field(name="Only set this to one specified in", value="<#501379425938571294>", inline = False)
            botmsg = await message.channel.send("", embed=embed)
            def check(m): return m.author == message.author
            try:
                callsign = await bot.wait_for('message', timeout=10, check=check)
                set_callsign(db, message.author, callsign.content)
                embed.add_field(name=u'\u2705', value=f'Callsign set to {callsign.content}', inline = False)
                await botmsg.edit(embed=embed)
                db[0].commit()
                db[0].close()
                break
            except asyncio.TimeoutError:
                embed.add_field(name=u'\u274C', value='Menu timed out', inline = False)
                await botmsg.edit(embed=embed)
                message.command.reset_cooldown(message)
                db[0].close()
                break
            break

    
    @_callsign.error
    async def _callsign_error(self, message, error):
        if isinstance(error, commands.CommandOnCooldown): await message.channel.send(f"Command on cooldown! Try again in {round(error.retry_after, 1)}s")


    @commands.command(name="status")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _status(self, message):
        while True:
            if check_channel(message.channel.id) == False: # Lines 17-23 are Check Func
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await message_wrong_channel.delete()
                await message.message.delete()
                break
            from config.confmain import dbconnect
            db = dbconnect()
            from assets.lib.functions.database import get_status, set_status
            status = get_status(db, message.author)
            if status == "Active": status = "Inactive"
            elif status == "Inactive": status = "Active"
            set_status(db, message.author, status)
            db[0].commit()
            db[0].close()
            await message.channel.send("", embed=discord.Embed(title=f":white_check_mark: Status set to: {status}", color=embedcolorlight))
            break

    @_status.error
    async def _status_error(self, message, error):
        if isinstance(error, commands.CommandOnCooldown): await message.channel.send(f"Command on cooldown! Try again in {round(error.retry_after, 1)}s")

    @commands.command(name="updaterank")
    async def update_roles(self, message):
        while True:
            if perm_check_superuser(message.author.id) == False: 
                logging.info(f"User {message.author.id} ran command reload and was denied!")
                msg_no_perms = await message.channel.send("Restricted!")
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
            users_1 = {}
            for user in message.guild.members:
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
            for user in message.guild.members:
                if users_2[str(user.id)] != users_1[str(user.id)]:
                    update_user_rank(db, user, users_1[str(user.id)])
                    update += 1
            await message.channel.send("", embed=discord.Embed(title=u"\u2705 Updated  "+str(update)+" user(s) with outdated ranks", color=errorcolor))
            db[0].commit()
            db[0].close()
            break
# For loading modules


def setup(bot):
    bot.add_cog(information_database_command(bot))