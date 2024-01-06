import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
import requests

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@tasks.loop(minutes=5)
async def update_nexus_info(embed, ggleap_token):
    AUTH_URL = 'https://api.ggleap.com/production/authorization/public-api/auth'
    BOOKINGS_URL = 'https://api.ggleap.com/beta/bookings/get-bookings'



    pass

@client.event
async def on_ready():
    base_embed = discord.Embed(color=discord.Color.from_str("#4E2A84"), 
                      title='Nexus Gaming Lounge Reservations',
                      type='rich')
    base_embed.add_field(name='Monday, 5-7PM', 
                    value='PCs 6-10 (VALORANT)')
    base_embed.add_field(name='Tuesday, 7-9PM', 
                    value='PC 3 (Overwatch)')
    base_embed.set_image(url='https://www.northwestern.edu/norris/arts-recreation/game-room/nexus-grand-opening025.jpg')
    ggleap_token = os.getenv("GGLEAP_TOKEN")
    update_nexus_info.start(base_embed, ggleap_token)

client.run(discord_token)