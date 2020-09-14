import discord
import json
import requests
import random
import datetime
import time
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

#Embed commands make the text look nicer when they are sent in group chats
#API must be updated every day 



#global variables
API = "RGAPI-496b6db7-9e20-4bf1-beba-350124923724"
watcher = LolWatcher(API)
my_region = "na1"
championURL = "http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json"
champions = requests.get(championURL).json()

def summonerID (summonerName):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summonerName+"?api_key="+API
    data = requests.get(URL).json()
    return data

def summonerMastery (ID):
    URL = "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + ID +"?api_key="+ API
    masteryData = requests.get(URL).json()
    return masteryData

@client.event 
async def on_ready(): 
    print ('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Sobble has a ping of {client.latency}' )

@client.command()
async def game(ctx):
    responses = [':dragon: League of Legends', 
                ':spy: Among us', 
                ':gun: Valorant',
                ':robot: Overwatch',
                ':ice_cube: Minecraft',
                ':book: Go Study Loser xD']

    embed = discord.Embed(
    description = random.choice(responses),             
    colour = discord.Colour.blue()
    )
    await ctx.send (embed=embed)

@client.command() #Finds Summoner Level
async def leagueXP(ctx, *, summonerName):
    responseXP = summonerID(summonerName)
    await ctx.send (f'Your summoner level is **{responseXP["summonerLevel"]}**')

@client.command() 
async def leagueTop(ctx, *, summonerName):
    responseMastery = summonerID(summonerName)
    ID = responseMastery['id']
    championMastery = summonerMastery(ID)
    for champion in champions['data']:
        if champions['data'][champion]['key'] == str(championMastery[0]['championId']):
            topPlayed = champions['data'][champion]['id']
            break
    
    lastPlayed = time.strftime('%Y-%m-%d @ %H:%M', time.localtime(int(championMastery[0]['lastPlayTime'])/1000))
 
    embed = discord.Embed(
    title = summonerName  ,
    description = "Top played champion: " + topPlayed + f"\nMastery Points: {championMastery[0]['championPoints']}" + "\nLast Playtime: " + lastPlayed ,              
    colour = discord.Colour.blue()
    )
    await ctx.send(embed=embed)

@client.command() #Finds League Rank and Percentile
async def leagueRank (ctx, *, summonerName):
    player = summonerID(summonerName)
    my_ranked_stats = watcher.league.by_summoner(my_region, player['id'])
    # await ctx.send (summonerName + ", your rank is : **"+ my_ranked_stats[0]['tier'] + " " + my_ranked_stats[0]['rank'] + "!**")
    #iron embles and percentiles
    if my_ranked_stats[0]['tier'] == "IRON": 
        if my_ranked_stats[0]['rank'] == "IV":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/1-1.png"
            percentile = "100"    
        elif my_ranked_stats[0]['rank'] == "III":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/1-1.png"
            percentile = "100"
        elif my_ranked_stats[0]['rank'] == "II":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/1-1.png"
            percentile = "99"
        elif my_ranked_stats[0]['rank'] == "I":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/1-1.png"
            percentile = "97"     
    #bronze emblems and percentiles                             
    elif my_ranked_stats[0]['tier'] =="BRONZE": 
        if my_ranked_stats[0]['rank'] == "IV":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/2-1.png"
            percentile = "94"    
        elif my_ranked_stats[0]['rank'] == "III":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/2-1.png"
            percentile = "89"
        elif my_ranked_stats[0]['rank'] == "II":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/2-1.png"
            percentile = "85"
        elif my_ranked_stats[0]['rank'] == "I":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/2-1.png"
            percentile = "79" 
    #silver emblems and percentiles
    elif my_ranked_stats[0]['tier'] =="SILVER": 
        if my_ranked_stats[0]['rank'] == "IV":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/3-1.png"
            percentile = "71"    
        elif my_ranked_stats[0]['rank'] == "III":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/3-1.png"
            percentile = "60"
        elif my_ranked_stats[0]['rank'] == "II":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/3-1.png"
            percentile = "52"
        elif my_ranked_stats[0]['rank'] == "I":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/3-1.png"
            percentile = "43"
    #gold emblems and percentiles
    elif my_ranked_stats[0]['tier'] =="GOLD": 
        if my_ranked_stats[0]['rank'] == "IV":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/4-1.png"
            percentile = "37"    
        elif my_ranked_stats[0]['rank'] == "III":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/4-1.png"
            percentile = "24.7"
        elif my_ranked_stats[0]['rank'] == "II":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/4-1.png"
            percentile = "18.6"
        elif my_ranked_stats[0]['rank'] == "I":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/4-1.png"
            percentile = "13.7"
    #platinum emblems and percentiles
    elif my_ranked_stats[0]['tier'] =="PLATINUM": 
        if my_ranked_stats[0]['rank'] == "IV":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/5-1.png"
            percentile = "10.9"    
        elif my_ranked_stats[0]['rank'] == "III":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/5-1.png"
            percentile = "5.95"
        elif my_ranked_stats[0]['rank'] == "II":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/5-1.png"
            percentile = "4.25"
        elif my_ranked_stats[0]['rank'] == "I":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/5-1.png"
            percentile = "3.18"           
    #diamond emblems and percentiles
    elif my_ranked_stats[0]['tier'] =="DIAMOND": 
        if my_ranked_stats[0]['rank'] == "IV":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/6-1.png"
            percentile = "1.99"    
        elif my_ranked_stats[0]['rank'] == "III":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/6-1.png"
            percentile = "0.89"
        elif my_ranked_stats[0]['rank'] == "II":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/6-1.png"
            percentile = "0.48"
        elif my_ranked_stats[0]['rank'] == "I":
            icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/6-1.png"
            percentile = "0.20"   
    #master emblems and percentiles        
    elif my_ranked_stats[0]['tier'] =="MASTER": 
        icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/7-1.png"
        percentile = "0.06"
    #grandmaster emblems and percentiles
    elif my_ranked_stats[0]['tier'] =="GRANDMASTER": 
        icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/8-1.png"
        percentile = "0.05"
    #challenger emblems and percentiles
    elif my_ranked_stats[0]['tier'] =="CHALLENGER": 
        icon = "https://lolg-cdn.porofessor.gg/img/league-icons-v2/160/9-1.png"
        percentile = "0.02"
    
    embed = discord.Embed (
        title = summonerName  , 
        description = summonerName + ", your rank is : **"+ my_ranked_stats[0]['tier'] + " " + my_ranked_stats[0]['rank'] + "!**\n" + "\nWhich makes you in the top **"+percentile+"%**!" ,              
        colour = discord.Colour.blue()
    )        
    
    embed.set_image (url = icon)    
    await ctx.send (embed=embed)
    
#finds random pictures of sobble!
@client.command()
async def sob (ctx):
    responses = ["https://cdn.bulbagarden.net/upload/thumb/9/9b/816Sobble.png/1200px-816Sobble.png", 
                 "https://cdn.bulbagarden.net/upload/thumb/d/db/Goh_Sobble.png/1200px-Goh_Sobble.png", 
                 "https://www.serebii.net/Shiny/SWSH/816.png", 
                 "https://media.comicbook.com/2020/07/pokemon-journeys-sobble-1227814-1280x0.jpeg", 
                 "https://cdn.vox-cdn.com/thumbor/Vg038cZnYl_JSqxay4OiR6TBuC0=/0x0:1429x762/1200x800/filters:focal(601x267:829x495)/cdn.vox-cdn.com/uploads/chorus_image/image/63136628/Screen_Shot_2019_02_27_at_11.26.15_AM.0.png", 
                 "https://media.comicbook.com/2020/07/pokemon-journeys-sobble-trainer-ash-goh-anime-1228761-1280x0.jpeg", 
                 "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/80ff523f-ff84-457d-a547-464588d3a3d3/de166tk-978cd659-836d-4a74-9157-5301c3b23fab.jpg/v1/fill/w_1024,h_576,q_75,strp/goh_s_2nd_galar_starter__sobble_by_willdinomaster55_de166tk-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD01NzYiLCJwYXRoIjoiXC9mXC84MGZmNTIzZi1mZjg0LTQ1N2QtYTU0Ny00NjQ1ODhkM2EzZDNcL2RlMTY2dGstOTc4Y2Q2NTktODM2ZC00YTc0LTkxNTctNTMwMWMzYjIzZmFiLmpwZyIsIndpZHRoIjoiPD0xMDI0In1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.h7u9yQ0wF_390fqOda5m5HyER7dOzFxCxCPjuSd9N60", 
                 "https://static.zerochan.net/Sobble.full.2506479.png", 
                 "https://static.zerochan.net/Sobble.full.2515461.png", 
                 "https://cdnb.artstation.com/p/assets/images/images/020/665/885/large/anh-dang-eeoyvkkxuammimv.jpg?1568695795"
                ]
    await ctx.send (random.choice(responses))


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print (f'{member} has left a server')

client.run('NzUyOTk0NjY1NDQ3MjkzMDM5.X1fu7g.yBTyueYoNzdERYshOacx2XoO0eA') 