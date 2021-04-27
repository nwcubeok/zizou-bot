import discord
import mysql.connector
import unicodedata
import threading
import asyncio
import random
import json
import time
import os
from discord.ext import commands
from discord.utils import get

"""
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "###",
    database = "member_list"
)
mycursor = db.cursor()
#mycursor.execute("CREATE DATABASE member_list")
"""

intents = discord.Intents.all()
intents.typing = True
intents.presences = True

TOKEN = 'ODIyNDkyMjk4MjgxMDkxMTQ0.YFTDpQ.eVrM6nd3CCFgE7ynCBmeGCahUUI'
bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)
client = discord.Client()

os.chdir("C:\\Users\\rayas\\Desktop\\bot")
@bot.event
async def on_ready():
    print('Connecté en tant que')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('~~~'))

#----------------------------------------------------------------------------------------------------------------------

def check_int(intervalle):
    for i in range(len(intervalle)):
        print("i:",i,"intervalle[i]:",intervalle[i],type(intervalle[i]))
        if intervalle[i] is not str():
            return False
    return True

def erreur(syntaxe):
    return "> \U0001F4A2 __**Erreur syntaxe:**__ "+syntaxe

def CONSOLE(*msg: None):
    return discord.Embed(title="```   CONSOLE   ```", color=0xfd3030, description=f"```> {' '.join(msg)}```")

#----------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    #await bot.change_presence(activity= discord.Game(message.content))
    await bot.process_commands(message)
    #print(message.author,":", message.content)

@bot.command(aliases = ['h','aide'])
async def help(ctx):
    help_msg = await ctx.send("__**Commandes disponibles:**__")
    for commande, info in help_list.items():
        await help_msg.edit(content=str(help_msg.content)+commande+info)

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong!  `{round(bot.latency*1000)}ms`")

@bot.command()
async def ensar(ctx): return await ctx.send("<:Nooko:825791586045526076><:Nooko:825791586045526076><:Nooko:825791586045526076><:Nooko:825791586045526076>")

@bot.command(pass_context=True)
async def gay(ctx):
    await ctx.send('<:Nooko:825791586045526076>')
    await ctx.message.delete()

@bot.command()
async def random(ctx):
    import random
    print(list(ctx.channel.guild.members))
    rdm = random.choice(list(ctx.channel.guild.members))
    await ctx.send(rdm)

@bot.command()
async def roles_add(ctx, *roles):
    print("> Executing roles_add")
    roles_list  = []
    import random
    for id in roles:
        if id == "0":
            roles_list.append((ctx.channel.guild.roles[-1]).id)
        else:
            roles_list.append(id[3:-1])
    for user in ctx.channel.guild.members:
        try:
            role = discord.utils.get(ctx.channel.guild.roles, id= int(random.choice(roles_list)))
            await user.add_roles(role)
        except:
            pass
    await ctx.send("> **Random roles** ("+', '.join(roles)+") were successfully added!")

@bot.command()
async def roles_remove(ctx, *roles):
    print("> Executing roles_remove")
    await ctx.message.delete()
    roles_list = []
    for id in roles:
        roles_list.append(id[3:-1])
    print(roles_list)
    for user in ctx.channel.guild.members:
        for i in range(len(roles_list)):
            print(i)
            role = discord.utils.get(ctx.channel.guild.roles, id= int(roles_list[i]))
            print(role)
            if role in user.roles: 
                await user.remove_roles(role)
                print(role)
                break
        i = 0
    await ctx.send("> **Random roles** ("+', '.join(roles)+") were successfully removed!")
    print("OKremove")

@bot.command(aliases = ['pc'])
async def pour_combien(ctx, lim, reverse, *gage):

    async def timer(time, msg_to_edit):
        while time >= 0:
            embed.set_footer(text=f"• {time} secondes restantes...\n\n\u270B Pour accepter     \u274c Pour annuler (seulement pour le créateur)")
            if stop_timer == 1: return
            time -= 1
            await asyncio.sleep(0.8)
            await msg_to_edit.edit(embed=embed)
        return

    async def jeu(rep_player1, rep_player2, limit, reverse_var, gagnant):

        # Initialisation et envoie du MP destiné aux joueurs
        if reverse_var == 0: msg_for_player = f"> Pour combien entre **{player1.name}** et **{player2.name}** avec comme gage: {gage}!\n> Ecrivez un nombre entre **1 et {limit}**:"
        else: msg_for_player = f"> __**REVERSE:**__ Pour combien entre **{player1.name}** et **{player2.name}** avec comme gage: {gage}!\n> Ecrivez un nombre entre **1 et {limit}**:"
        for player in [player1,player2]: await player.send(msg_for_player)

        # Vérification et enregistrement du nombre donné par le joueur par message privé 
        while True:
            try: nombre = await bot.wait_for('message', timeout=60, check=lambda nombre: nombre)
            except asyncio.TimeoutError: return await console.edit(embed= CONSOLE("END: Un ou les joueurs n'ont pas donné de nombre..."))
            else:
                if isinstance(nombre.channel, discord.DMChannel):
                    if nombre.author == player1:
                        if nombre.content.isnumeric() == False or int(nombre.content) > int(limit) or int(nombre.content) < 1:
                            await player1.send(f"> Votre nombre doit se situer entre **1 et {limit}**!")
                        else:
                            await player1.send("> Votre réponse a été enregistrée!")
                            await console.edit(embed= CONSOLE(f"✓ | {player1.name} a confirmé son choix! "))
                            rep_player1 = nombre.content
                    elif nombre.author == player2:
                        if nombre.content.isnumeric() == False or int(nombre.content) > int(limit) or int(nombre.content) < 1:
                            await player2.send(f"> Votre nombre doit se situer entre **1 et {limit}**!")
                        else:
                            await player2.send("> Votre réponse a été enregistrée!")
                            await console.edit(embed= CONSOLE(f"✓ | {player2.name} a confirmé son choix! "))
                            rep_player2 = nombre.content
                    if rep_player1 != None and rep_player2 != None: break

        # Animation de l'affichage des résultats
        await asyncio.sleep(2)
        await console.edit(embed= CONSOLE(f"Affichage des résultats... "))
        embed_resultats = await ctx.send(embed= EMBED_RESULTATS("...","..."))
        await asyncio.sleep(4)
        await embed_resultats.edit(embed= EMBED_RESULTATS(f"**{int(rep_player1)}** !","..."))
        await asyncio.sleep(4)
        await embed_resultats.edit(embed= EMBED_RESULTATS(f"**{int(rep_player1)}** !",f"**{int(rep_player2)}** !"))
        await asyncio.sleep(1.5)

        # Vérifications des résultats et du reverse donné au départ
        if int(rep_player1) == int(rep_player2):
            if gagnant == 1: return await ctx.send(f"> 🎉 **{player1.name} a gagné!**\n> {player2.name} doit *{gage}*!")
            else: return await ctx.send(f"> 🎉 **{player2.name} a gagné!**\n> {player1.name} doit *{gage}*!")
        elif reverse_message == "avec" and gagnant == 1:
            reverse, new_limit = False, int(limit)//2
            if new_limit == 1: new_limit = 2
            await ctx.send("> Les 2 joueurs n'ont pas eu la même réponse, **reverse** en cours...!")
            return await jeu(None,None,new_limit,1,2)
        elif reverse_message == "infini":
            if gagnant == 1: return await jeu(None,None,new_limit,1,2) 
            else: return await jeu(None,None,new_limit,1,1)
        else: return await ctx.send("> Personne n'a gagné...")

    def EMBED_RESULTATS(nb1, nb2): 
        return discord.Embed(title=f"``` Résultats du pour combien ```", description=f"{player1.name} a choisi {nb1}\n\n{player2.name} a choisi {nb2}", color=0x3be376)

    # Initialisation des variables
    syntaxe_commande = "?pour_combien [limite: *nombre (> 1)*] [reverse: *True/False/Infini*] [defi: *texte*]"
    gage = ' '.join(gage)
    stop_timer, time = 0, 30

    # Tester les variables données par l'utilisateur
    if str(lim).isnumeric() == False: return await ctx.send(erreur(syntaxe_commande))
    elif int(lim) < 1: return await ctx.send(erreur(syntaxe_commande))
    elif reverse == str(True): reverse_message = "avec"
    elif reverse == str(False): reverse_message = "sans"
    elif reverse == "Infini": reverse_message = "infini"
    else: return await ctx.send(erreur(syntaxe_commande))

    # Création embed pour combien,console
    embed = discord.Embed(
        title=f"``` Pour-Combien lancé par {ctx.message.author.name}            ```",
        description="> {} \n ```Paramètres: Entre 1 et {}, {} reverse.```".format(gage,lim,reverse_message),
        color = discord.Color.blue()
        )
    embed.set_footer(text=f"• {time} secondes restantes...\n\n\u270B Pour accepter     \u274c Pour annuler (seulement pour le créateur)")
    embed.set_thumbnail(url= ctx.message.author.avatar_url)
    demande = await ctx.send(embed= embed)
    console = await ctx.send(embed= CONSOLE("..."))

    # Lancement du timer pendant que la fonction continue de s'executer + réactions
    bot.loop.create_task(timer(time, demande))
    await asyncio.sleep(2)
    await demande.add_reaction("\u270B")
    await demande.add_reaction("\u274c")

    # Verification de l'ajout de réaction (le "While True" permet de réexecuter le "wait_for" si la réaction ne convient pas)
    while True: 
        try: reaction, user = await bot.wait_for('reaction_add', timeout=time, check=lambda reaction, user: reaction.emoji in [u'\u270B',u'\u274c']) 
        except asyncio.TimeoutError: return await console.edit(embed= CONSOLE("END: Personne n'a accepté...")) 
        else:
            if user == bot.user: pass
            else:
                if reaction.emoji == u'\u270B':
                    if user != ctx.author: break
                    else: await console.edit(embed= CONSOLE(f"{user.name} ne peut pas participer..."))
                else:
                    if user == ctx.author:
                        stop_timer = 1
                        return await console.delete()
                    else: await console.edit(embed= CONSOLE(f"{user.name} ne peut pas annuler..."))

    # Arrêt du timer et mise en place des player 1 et 2
    stop_timer = 1
    player1, player2 = ctx.message.author, user
    
    # Appel de la fonction pour commencer le jeu et la fin de la fonction
    await jeu(None,None,lim,0,1)
    return await console.delete()


#----------------------------------------------------------------------------------------------------------------------

@bot.command()
async def test(ctx):
    await ctx.send(bot.command_prefix)

@bot.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.send("👋")
    await bot.logout()

p = bot.command_prefix
help_list = {
    f"``` {p}help | Alias: {', '.join(help.aliases)}```" : "Affiche la liste des commandes. __Syntaxe:__ ?help <commande>",
    f"``` {p}ping | Alias: {', '.join(ping.aliases)}```" : "Affiche le ping du bot en ms. __Syntaxe:__ ?ping"
    }
    

bot.run(TOKEN)



