import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
import requests
import datetime
import json

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class BookingClient(discord.Client):
    def __init__(self, client):
        self.client = client
        self.client.booking_channel = 0
        self.tree = discord.app_commands.CommandTree(self)
        self.config = {}
        with open('config.json', 'w+') as file:
            file.seek(0, os.SEEK_END)
            if file.tell():
                file.seek(0)
                self.config = json.load(file)

client = BookingClient(intents=intents)

@client.event
async def on_guild_join(self, guild):
    if guild.id not in self.config:
        self.config[guild.id] = {'ggleap': '', 'channel_id': 0, 'message_id': 0, 'editor_role': 'Leadership'}
    pass

@tasks.loop(minutes=5)
async def update_nexus_info(embed, ggleap_token):
    AUTH_URL = 'https://api.ggleap.com/production/authorization/public-api/auth'
    BOOKINGS_URL = 'https://api.ggleap.com/beta/bookings/get-bookings'
    MACHINES_URL = 'https://api.ggleap.com/beta/machines/get-all'
    ggleap_token = client.config['Guild ID Goes Here']['ggleap']
    
    #do all the ggleap requests
    auth = requests.post(AUTH_URL, data={'AuthToken':ggleap_token}).json()
    auth = auth['Jwt']

    header = {"Content-Type": "application/json", "Authorization": auth}

    bookings_payload = {'Date': datetime.date.today().isoformat()}
    bookings = requests.get(BOOKINGS_URL, bookings_payload, headers=header).json()
    machines = requests.get(MACHINES_URL, headers=header).json()

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

@client.tree.command(description = 'Edit bot configuration')
async def config(interaction: discord.Interaction, ggleap='', channel_id = 0, editor_role = ''):
    guild_id = interaction.guild_id
    if ggleap != '':
        client.config[guild_id]['ggleap'] = ggleap
    if editor_role != '':
        client.config[guild_id]['editor_role'] = editor_role
    if channel_id != 3:
        client.config[guild_id]['channel_id'] = channel_id
    with open('config.json', 'w+') as file:
        json.dump(client.config, file)
        file.truncate()

client.run(discord_token)