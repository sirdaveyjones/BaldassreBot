import discord
from discord import app_commands
import os

client = discord.Client(intents = discord.Intents.default())

class Services(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self): # prints ready message to console
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 1018990233959813140))
            self.synced = True
        print(f"Bot Online!")        

client = aclient()
tree = app_commands.CommandTree(client)

# await interaction.response.send_message()

@tree.command(name = "interest_rate", description = "Set the CDP base interest rate.", guild = discord.Object(id = 1018990233959813140))
async def interest_rate(interaction: discord.Interaction, rate: str):
    await interaction.response.send_message(f"Base interest assigned!", ephemeral = True)
    
@tree.command(name = "services", description = "Create services window in the assigned channel.", guild = discord.Object(id = 1018990233959813140))
async def services(interaction: discord.Interaction, base_int: float, alliance_loans: bool, pers_loans: bool, discord_ads: bool, ig_ads: bool, econ_sheets: bool):
    await interaction.response.send_message(f"Your window is being created!", ephemeral = True)
    interest_low =  base_int*0.895
    interest_high = base_int*1.75
    if alliance_loans == True:
        circle1 = ':green_circle:'
        availability1 = 'Available'
    if alliance_loans == False:
        circle1 = ':red_circle:'
        availability1 = 'Unavailable'
    if pers_loans == True:
        circle2 = ':green_circle:'
        availability2 = 'Available'
    if pers_loans == False:
        circle2 = ':red_circle:'
        availability2 = 'Unavailable'
    if discord_ads == True:
        circle3 = ':green_circle:'
        availability3 = 'Available'
    if discord_ads == False:
        circle3 = ':red_circle:'
        availability3 = 'Unavailable'
    if ig_ads == True:
        circle4 = ':green_circle:'
        availability4 = 'Available'
    if ig_ads == False:
        circle4 = ':red_circle:'
        availability4 = 'Unavailable'
    if econ_sheets == True:
        circle5 = ':green_circle:'
        availability5 = 'Available'
    if econ_sheets == False:
        circle5 = ':red_circle:'
        availability5 = 'Unavailable'
    embed = discord.Embed(title="CDP Financial - Service Status", description="""**Current Interest Rates**
    Base Interest: """ + str('{:.1%}'.format(base_int)) + """
    Interest Range: """ + str('{:.1%}'.format(interest_low)) + " - " + str('{:.1%}'.format(interest_high)) + """
    
    
    **Availability**
    """ + circle1 + " **| Alliance Loans:** " + availability1 + """
    """ + circle2 + " **| Personal Loans:** " + availability2 + """
    """ + circle3 + " **| Discord Advertisements:** " + availability3 + """
    """ + circle4 + " **| In-Game Advertisements:** " + availability4 + """
    """ + circle5 + " **| Econ Sheets:** " + availability5 + """
    

    :green_circle: - Available
    :red_circle: - Unavailable""", color =  0x0400ff)   
    channel = client.get_channel(1019614707394556025)
    await channel.send(embed=embed, view=Services())

client.run('REDACTED')
