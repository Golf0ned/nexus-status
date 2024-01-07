import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class BookingClient(discord.Client):
    def __init__(self, client):
        self.client = client
        self.client.booking_channel = 0

client = BookingClient(intents=intents)

@tasks.loop(minutes=5)
async def update_nexus_info(embed, ggleap_token):
    AUTH_URL = 'https://api.ggleap.com/production/authorization/public-api/auth'
    BOOKINGS_URL = 'https://api.ggleap.com/beta/bookings/get-bookings'
    ggleap_token = os.getenv("GGLEAP_TOKEN")
    
    #do all the ggleap requests
    auth = requests.post(AUTH_URL, data={'AuthToken':ggleap_token}).json()
    auth = auth['Jwt']

    header = {"Content-Type": "application/json", "Authorization": auth}

    bookings_payload = {'Date': datetime.date.today().isoformat()}
    bookings = requests.get(BOOKINGS_URL, bookings_payload, headers=header).json()

    #update embed
    embed.add_field(name='Monday, 5-7PM', 
                    value='PCs 6-10 (VALORANT)')
    
    #

    pass

@client.event
async def on_ready():
    base_embed = discord.Embed(color=discord.Color.from_str("#4E2A84"), 
                      title='Nexus Gaming Lounge Reservations',
                      type='rich')
    base_embed.set_image(url='https://www.northwestern.edu/norris/arts-recreation/game-room/nexus-grand-opening025.jpg')
    ggleap_token = os.getenv("GGLEAP_TOKEN")
    update_nexus_info.start(base_embed, ggleap_token)

client.run(discord_token)