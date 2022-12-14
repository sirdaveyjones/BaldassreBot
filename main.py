import discord
from discord import app_commands
import os
import pymysql

client = discord.Client(intents = discord.Intents.all())

cdp_db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'cdp',
    autocommit = True
)

cursor = cdp_db.cursor()

class Services(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

class ticket_embed(discord.ui.View):
	def __init__(self) -> None:
        	super().__init__(timeout=None)

	@discord.ui.button(label = "Alliance Loan App.", style = discord.ButtonStyle.blurple, custom_id = "alliance_loan")
	async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
		ticket = discord.utils.get(interaction.guild.text_channels, name = f"{interaction.user.name.lower().replace(' ', '-')}-alliance-loan")
		if ticket is not None: await interaction.response.send_message(f"You already have a Loan Application open!", ephemeral = True)
		else:
			overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages = True, view_channel = True),
            interaction.guild.get_role(991903963744047197): discord.PermissionOverwrite(read_messages = True, view_channel = True),
        }
			channel_cat = discord.utils.get(interaction.guild.categories, id=966697552588201994)
			channel = await interaction.guild.create_text_channel(name = f"{interaction.user.name}-alliance-loan", category = channel_cat, overwrites=overwrites) # Problematic Line
			await channel.send(f"""Here is your Loan Application ticket, {interaction.user.mention}!
            
Use the `/application` command to provide our staff with needed information regarding your loan. This will be the baseline that our staff uses to establish your eligibility for a loan with us.""")
			await interaction.response.defer()
        
	@discord.ui.button(label = "Personal Loan App.", style = discord.ButtonStyle.grey, custom_id = "personal_loan")
	async def ticket2(self, interaction: discord.Interaction, button: discord.ui.Button):
		ticket = discord.utils.get(interaction.guild.text_channels, name = f"{interaction.user.name.lower().replace(' ', '-')}-personal-loan")
		if ticket is not None: await interaction.response.send_message(f"You already have a Loan Application open!", ephemeral = True)
		else:
			overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages = True, view_channel = True),
            interaction.guild.get_role(991903963744047197): discord.PermissionOverwrite(read_messages = True, view_channel = True),
        }
			channel_cat = discord.utils.get(interaction.guild.categories, id=996859448133959710)
			channel = await interaction.guild.create_text_channel(name = f"{interaction.user.name}-personal-loan", category = channel_cat,  overwrites=overwrites) # Problematic Line
			await channel.send(f"""Here is your Loan Application ticket, {interaction.user.mention}!
            
Use the `/application` command to provide our staff with needed information regarding your loan. This will be the baseline that our staff uses to establish your eligibility for a loan with us.

*Reminder: If you have fewer than 18 Cities, you are not eligible for a loan with CDP Financial. There are no exceptions made.""")
			await interaction.response.defer()
	@discord.ui.button(label = "Advertising", style = discord.ButtonStyle.red, custom_id = "advertising")
	async def ticket3(self, interaction: discord.Interaction, button: discord.ui.Button):
		ticket = discord.utils.get(interaction.guild.text_channels, name = f"{interaction.user.name.lower().replace(' ', '-')}-advertising")
		if ticket is not None: await interaction.response.send_message(f"You already have an Advertising ticket open!", ephemeral = True)
		else:
			overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages = True, view_channel = True),
        }
			channel_cat = discord.utils.get(interaction.guild.categories, id=996924177258921994)
			channel = await interaction.guild.create_text_channel(name = f"{interaction.user.name}-advertising", category = channel_cat, overwrites=overwrites) # Problematic Line
			await channel.send(f"Here is your ticket, {interaction.user.mention}!")
			await interaction.response.defer()

	@discord.ui.button(label = "Econ Sheet", style = discord.ButtonStyle.green, custom_id = "econ_sheet")
	async def ticket4(self, interaction: discord.Interaction, button: discord.ui.Button):
		ticket = discord.utils.get(interaction.guild.text_channels, name = f"{interaction.user.name.lower().replace(' ', '-')}-econ-sheet")
		if ticket is not None: await interaction.response.send_message(f"You already have an Econ Sheet ticket open!", ephemeral = True)
		else:
			overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages = True, view_channel = True),
        }
			channel_cat = discord.utils.get(interaction.guild.categories, id=996924177258921994)
			channel = await interaction.guild.create_text_channel(name = f"{interaction.user.name}-econ-sheet", category = channel_cat, overwrites=overwrites) # Problematic Line
			await channel.send(f"Here is your ticket, {interaction.user.mention}!")
			await interaction.response.defer()

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.added = False

    async def on_ready(self): # prints ready message to console
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 966502687925497866))
            self.synced = True
        if not self.added:
            self.add_view(ticket_embed())
            self.added = True
        activity = discord.Activity(name="Arc embezzle!", type=3)
        await client.change_presence(status=discord.Status.online, activity=activity)
        print(f"Bot Online!")        

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = "tickets", description = "Launch the ticketing system!")
async def ticketing(interaction: discord.Interaction):
    embed = discord.Embed(title = "Available CDP Services", description = "Use the buttons below to open a ticket to discuss your new Alliance Loan, Personal Loan, Advertising Campaign, or Custom Econ Sheet!",color = 0x0400ff)
    await interaction.channel.send(embed = embed, view = ticket_embed())
    await interaction.response.send_message("Ticket system has been launched!", ephemeral = True)

@tree.command(name = "application", description = "Apply for a loan with CDP Financial", guild = discord.Object(id = 966502687925497866))
async def loan_app(interaction: discord.Interaction, nation_id: int, amt_requested: float, interest_requested: float, weeks: int):
    total_interest = ((interest_requested*amt_requested/(1-(1+interest_requested)**-weeks))*weeks)-amt_requested
    weekly_pmt = (total_interest + amt_requested)/weeks
    embed = discord.Embed(title="CDP Financial - Loan Application", url = 'https://politicsandwar.com/nation/id='+str(nation_id), description= "**Applicant ID:** " + str(nation_id) + """
    **Principle Requested:** """ + str('${:,.2f}'.format(amt_requested)) + """
    **Requested Repayment Term:** """ + str(weeks) + """ Weeks
    **Requested Interest Rate:** """ + str('{:.1%}'.format(interest_requested)) + """
    
    **Calculated Total Interest:** """ + str('${:,.2f}'.format(total_interest)) + """
    **Calculated Payments:** """ + str('${:,.2f}'.format(weekly_pmt)), color = 0x400ff)
    sql = "INSERT INTO loans (ID, PRINCIPLE, INTEREST, BALANCE, ACTIVE) VALUES (%s, %s, %s, %s, %s)"
    val = (nation_id, amt_requested, interest_requested, (total_interest + amt_requested), 0)
    cursor.execute(sql, val)
    await interaction.response.send_message(embed=embed)

@tree.command(name = "accept", description = "Accept a loan application!", guild = discord.Object(id = 966502687925497866))
async def accept_loan(interaction: discord.Interaction, nation_id: int, interest: float):
    sql = "UPDATE loans SET ACTIVE = '1' where ID = (%s)"
    val = (nation_id)
    cursor.execute(sql,val)
    get_balance = "SELECT `BALANCE` FROM `loans` WHERE `ID`=%s"
    cursor.execute(get_balance, (nation_id,))
    balance = cursor.fetchone()
    balance = str(balance).replace("(", "")
    balance = balance.replace(")","")
    balance = balance.replace("'","")
    balance = balance.replace(",","")
    embed = discord.Embed(title="CDP Financial - Loan Issuance", description="""
    Thank you for requesting a loan with CDP Financial. The loan has been approved on the following terms.

    **Applicant ID:** """ + str(nation_id) + """
    **Current Balance:** """ + str('${:,.2f}'.format(float(balance))) + """
    **Interest Rate:** """ + str('{:.1%}'.format(interest)), color =  0x0400ff)
    await interaction.response.send_message(embed=embed)

#async def dbtest(interaction: discord.Interaction):
#    sql = "INSERT INTO loans (ID, PRINCIPLE, INTEREST, BALANCE) VALUES (%s, %s, %s, %s)"
#    val = ("2065198416516161616165165163", "50", "100", "200")
#    cursor.execute(sql, val)

# class application(discord.ui.View):
#    def __init__(self):
#        super().__init__(timeout=None)

#    @discord.ui.button(label = "Approve", style = discord.ButtonStyle.green, custom_id = "approved")
#    async def approveloan(self, interaction: discord.Interaction, button: discord.ui.Button):
#        sql2 = "UPDATE loans SET ACTIVE = '1' where ID = (%s)"
#        val = (applicant_id)
#        cursor.execute(sql2,val)
#        await interaction.response.defer()

#    @discord.ui.button(label = "Deny", style = discord.ButtonStyle.red, custom_id = "denied")
#    async def denyloan(self, interaction: discord.Interaction, button: discord.ui.Button):
#        await interaction.response.defer()

@tree.command(name = "services", description = "Create services window in the assigned channel.", guild = discord.Object(id = 966502687925497866))
async def services(interaction: discord.Interaction, base_int: float, alliance_loans: int, pers_loans: int, discord_ads: int, ig_ads: int, econ_sheets: int):
    await interaction.response.send_message(f"Your window is being created!", ephemeral = True)
    interest_low =  base_int*0.895
    interest_high = base_int*1.75
    if alliance_loans == 1:
        circle1 = ':green_circle:'
        availability1 = 'Available'
    elif alliance_loans == 2:
        circle1 = ':yellow_circle:'
        availability1 = 'Limited Availability'
    elif alliance_loans == 3:
        circle1 = ':red_circle:'
        availability1 = 'Unavailable'
    if pers_loans == 1:
        circle2 = ':green_circle:'
        availability2 = 'Available'
    elif pers_loans == 2:
        circle2 = ':yellow_circle:'
        availability2 = 'Limited Availability'
    elif pers_loans == 3:
        circle2 = ':red_circle:'
        availability2 = 'Unavailable'
    if discord_ads == 1:
        circle3 = ':green_circle:'
        availability3 = 'Available'
    elif discord_ads == 2:
        circle3 = ':yellow_circle:'
        availability3 = 'Limited Availability'
    elif discord_ads == 3:
        circle3 = ':red_circle:'
        availability3 = 'Unavailable'
    if ig_ads == 1:
        circle4 = ':green_circle:'
        availability4 = 'Available'
    elif ig_ads == 2:
        circle4 = ':yellow_circle:'
        availability4 = 'Limited Availability'
    elif ig_ads == 3:
        circle4 = ':red_circle:'
        availability4 = 'Unavailable'
    if econ_sheets == 1:
        circle5 = ':green_circle:'
        availability5 = 'Available'
    elif econ_sheets == 2:
        circle5 = ':yellow_circle:'
        availability5 = 'Limited Availability'
    elif econ_sheets == 3:
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
    :yellow_circle: - Limited Availability
    :red_circle: - Unavailable""", color =  0x0400ff)   
    channel = client.get_channel(992056050503135333)
    global servicesembed
    servicesembed = await channel.send(embed=embed, view=Services())

@tree.command(name = "edit_service", description = "Edit the services window.", guild = discord.Object(id = 966502687925497866))
async def edit_service(interaction: discord.Interaction, base_int: float, alliance_loans: int, pers_loans: int, discord_ads: int, ig_ads: int, econ_sheets: int):
    await interaction.response.send_message(f"Your window is being edited!", ephemeral = True)
    interest_low =  base_int*0.895
    interest_high = base_int*1.75
    if alliance_loans == 1:
        circle1 = ':green_circle:'
        availability1 = 'Available'
    elif alliance_loans == 2:
        circle1 = ':yellow_circle:'
        availability1 = 'Limited Availability'
    elif alliance_loans == 3:
        circle1 = ':red_circle:'
        availability1 = 'Unavailable'
    if pers_loans == 1:
        circle2 = ':green_circle:'
        availability2 = 'Available'
    elif pers_loans == 2:
        circle2 = ':yellow_circle:'
        availability2 = 'Limited Availability'
    elif pers_loans == 3:
        circle2 = ':red_circle:'
        availability2 = 'Unavailable'
    if discord_ads == 1:
        circle3 = ':green_circle:'
        availability3 = 'Available'
    elif discord_ads == 2:
        circle3 = ':yellow_circle:'
        availability3 = 'Limited Availability'
    elif discord_ads == 3:
        circle3 = ':red_circle:'
        availability3 = 'Unavailable'
    if ig_ads == 1:
        circle4 = ':green_circle:'
        availability4 = 'Available'
    elif ig_ads == 2:
        circle4 = ':yellow_circle:'
        availability4 = 'Limited Availability'
    elif ig_ads == 3:
        circle4 = ':red_circle:'
        availability4 = 'Unavailable'
    if econ_sheets == 1:
        circle5 = ':green_circle:'
        availability5 = 'Available'
    elif econ_sheets == 2:
        circle5 = ':yellow_circle:'
        availability5 = 'Limited Availability'
    elif econ_sheets == 3:
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
    :yellow_circle: - Limited Availability
    :red_circle: - Unavailable""", color =  0x0400ff)   
    channel = client.get_channel(992056050503135333)
    global servicesembed
    servicesembed = await servicesembed.edit(embed=embed, view=Services())

#my_secret = os.environ['CDP']
#client.run(my_secret)

