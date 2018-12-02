# Modules

import discord, sys, asyncio, logging, traceback, time, os, random
from discord.ext.commands import Bot
from discord.ext import commands
from config.confmain import cwd, cwdmain, embedcolordark, embedcolorlight, errorcolor, check_channel, Client

# Games using the random lib as main functionality
class random_game:
    def __init__(self, bot): self.bot = bot
    
    # Russian Roulette
    @commands.command(name="russian")
    async def _russian(self, message, *args):
        while True:
            if check_channel(message.channel.id) == False: # Lines 16-22 Check Function
                logging.info(f"User {message.author.id} tried to run a command in the wrong channel!")
                msg_wrong_channel = await message.channel.send("You can't do Commands in this channel!")
                time.sleep(3)
                await msg_wrong_channel.delete()
                await message.message.delete()
                break  
            players = []  # Lines 23 - 31 Get users, and make a list
            for user_iter in list(args):
                player_add_id = ""
                for letter_iter in range(len(user_iter)):
                    if not(user_iter[letter_iter].isdigit()): pass
                    else: player_add_id += user_iter[letter_iter]
                try: player_add = self.bot.get_user(int(player_add_id))
                except: pass
                if not(player_add in players): players.append(player_add)
            if not(message.author in players): players.append(message.author)
            deadroll = random.randint(1, len(players)) # Lines 32 - TBC Game
            if len(players) < 2: 
                await message.channel.send("", embed=discord.Embed(title=u"\u274C You need 2+ People to play!", color=errorcolor))
                break
            title = "🔫 Russian roulette"
            embed = discord.Embed(title=title, description="Rolling in 3", color=embedcolorlight)
            botmsg = await message.channel.send("", embed=embed)
            played = []
            time.sleep(1)
            await botmsg.edit(embed = discord.Embed(title=title, description="Rolling in 2", color=embedcolorlight))
            time.sleep(1)
            await botmsg.edit(embed = discord.Embed(title=title, description="Rolling in 1", color=embedcolorlight))
            random.shuffle(players)
            time.sleep(1)

            for round in range(len(players)):
                await botmsg.edit(embed = discord.Embed(title=title, description=f"Round {round+1}: {players[round].name}#{players[round].discriminator}", color=embedcolorlight))
                time.sleep(1.5)
                await botmsg.edit(embed = discord.Embed(title=title, description=f"Round {round+1}: {players[round].name}#{players[round].discriminator}\n:click: .", color=embedcolorlight))
                time.sleep(1.5)
                await botmsg.edit(embed = discord.Embed(title=title, description=f"Round {round+1}: {players[round].name}#{players[round].discriminator}\n:click: ..", color=embedcolorlight))
                time.sleep(1.5)
                await botmsg.edit(embed = discord.Embed(title=title, description=f"Round {round+1}: {players[round].name}#{players[round].discriminator}\n:click: ...", color=embedcolorlight))
                if round+1 == deadroll:
                    await botmsg.edit(embed = discord.Embed(title=title, description=f"Round {round+1}: {players[round].name}#{players[round].discriminator}\n:click: 💥 BANG, You die!", color=embedcolorlight))
                    deaduser = players[round]       
                    time.sleep(2)
                    break
                else: await botmsg.edit(embed = discord.Embed(title=title, description=f"Round {round+1}: {players[round].name}#{players[round].discriminator}\n:click: POOF, You Live", color=embedcolorlight))
                time.sleep(2)
            alive = []
            for user in players:
                if not(user == deaduser): alive.append(user)
            alivestr = ""
            for user in alive: alivestr += f"\n     {user.name}#{user.discriminator}"
            await botmsg.edit(embed = discord.Embed(title=title, description=f"Alive : {alivestr}\nDead : \n    {deaduser.name}#{deaduser.discriminator} [Round {round+1}]", color=embedcolorlight))
            break

#For Loading Modules

def setup(bot):
    bot.add_cog(random_game(bot))