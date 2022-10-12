import discord
from discord.ext import commands
from discord.ui import InputText, Modal
import random 
import gspread
import datetime 
import time

#####################################################setup#####################################################
intents = discord.Intents.default()
intents.members = True

#####################################################Sheet set up#####################################################
gc = gspread.service_account(filename='')
sh = gc.open_by_url(")
bot = commands.Bot(command_prefix='$', case_insensitive=True, intents=intents)
now = datetime.datetime.now()
#####################################################variables#####################################################
column = -1
number = 0000
active_op = False
attend = 1111
id_num = 00
row = 4
red = 0xe74c3c
green = 0x2ecc71
idrow = 2
#####################################################setup#####################################################






class MyModal(Modal):
    def __init__(self) -> None:
        super().__init__("Operation Attendance Code")
        self.add_item(InputText(label="Attendance Code", placeholder="0000", min_length=4, max_length=4))
        self.add_item(InputText(label="ID Number", placeholder="0000", max_length=2))

       

    async def callback(self, interaction: discord.Interaction):
        global attend
        global column
        global row
        global number
        id_column = column + 1
        attend = int(self.children[0].value)
        id_num = self.children[1].value

        if attend == number:
            embed = discord.Embed(title="Attendance Logged", color=green)
            row = row + 1 
            worksheet = sh.worksheet("Attendance")
            worksheet.update_cell(row, column, attend)
            worksheet.update_cell(row, id_column, id_num)
        else:
            embed = discord.Embed(title="Incorrect Code", color=red)
        await interaction.response.send_message(embeds=[embed])


class profile(Modal):
    def __init__(self) -> None:
        super().__init__("Create VIS Member Profile")
        self.add_item(InputText(label="Operator Name", placeholder="What do you want to go by?", max_length=16))
        self.add_item(InputText(label="Age", placeholder="18", max_length=2))
        self.add_item(InputText(label="Timezone", placeholder="CST", max_length=4))
        self.add_item(InputText(label="Specialty", placeholder="Medical, Infantry, Pilot, Marksman, etc", required=False))

    async def callback(self, interaction: discord.Interaction):
        global idrow
        global added_to_roster
        name = self.children[0].value
        age = int(self.children[1].value)
        timezone = self.children[2].value
        special = self.children[3].value
        now = datetime.datetime.now()
        date = now.strftime("%m-%d-%y")
       
        idrow = idrow + 1 
        worksheet = sh.worksheet("Roster")
        worksheet.update_cell(idrow, 1, name)
        worksheet.update_cell(idrow, 2, age)
        worksheet.update_cell(idrow, 3, timezone)
        worksheet.update_cell(idrow, 4, special)
        worksheet.update_cell(idrow, 5, date)
        embed = discord.Embed(title="Thank you!", color=green)
        await interaction.response.send_message(embeds=[embed])
        
        

    

#####################################################Bot#####################################################
@bot.slash_command(name="opstart", guild_ids=[])
async def opstart(ctx):
    global column
    global number
    global active_op 
    column = column + 2
    number = random.randint(1000,9999)

    now = datetime.datetime.now()
    date = now.strftime("%m-%d-%y")
    time_now = now.strftime("%H:%M")
    worksheet = sh.sheet1
    worksheet.update_cell(1, column, date)
    worksheet.update_cell(2, column, time_now)
    active_op = True

    embed = discord.Embed(title=f'Operation Attendence Created', colour=ctx.author.colour)

    embed.add_field(name='The attendance code is:', value=number)
    embed.add_field(name='Tsheet:', value=column)

    embed.set_footer(text=f"{bot.user.name}")
    embed.set_author(name=bot.user.name)

    await ctx.respond(embed=embed)
    

@bot.slash_command(name="opattend", guild_ids=[])
async def opattend(ctx):
    global number
    if active_op == True:
        modal = MyModal()
        await ctx.interaction.response.send_modal(modal)
    else:
        embed = discord.Embed(title=f'Operation has ended', colour=ctx.author.colour)
        embed.set_footer(text=f"{bot.user.name}")
        embed.set_author(name=bot.user.name)
        await ctx.respond(embed=embed)

  

@bot.slash_command(name="opend", guild_ids=[])
async def opend(ctx):
    global column
    global number
    global active_op 
    global row

    embed = discord.Embed(title=f'{bot.user.name} Operation ended', colour=ctx.author.colour)
    await ctx.respond(embed=embed)
    later = datetime.datetime.now()
    time_later = later.strftime("%H:%M")
    worksheet = sh.worksheet("Attendance")
    worksheet.update_cell(3, column, time_later)
    active_op = False
    row = 4

@bot.slash_command(name="myid", description="Find my VIS id number", guild_ids=[])
async def createid(ctx):
    idnum = int(ctx.author.id)
    fourid = (idnum % 1000)

    embed = discord.Embed(title=f'', colour=ctx.author.colour)

    embed.add_field(name='Your ID number is:', value=fourid)
    embed.set_footer(text=f"{bot.user.name}")
    embed.set_author(name=bot.user.name)

    await ctx.respond(embed=embed)

@bot.slash_command(name="apply", guild_ids=[])
async def apply(ctx):
    global idrow
    idrow_off = idrow + 1
    modal = profile()
    await ctx.interaction.response.send_modal(modal)
    userid = str(ctx.author.id)
    worksheet = sh.worksheet("Roster")
    worksheet.update_cell(idrow_off, 6, userid)
    #member = discord.member
    #role = discord.utils.get(member.guild.roles, name="Junior Operator")
    await member.add_roles(role)

    


#@bot.slash_command(name="search", guild_ids=[902378457382649918])
#async def search(ctx):
#    userid = str(ctx.author.id)
#    worksheet = sh.worksheet("Sheet2")
#    find = worksheet.find("12555222")

#    print(find)

    
#####################################################runs bat#####################################################
bot.run()




















