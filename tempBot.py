import discord, pathlib
from discord.ext import commands
import json, os, sys, random


PATH = pathlib.Path(__file__).parent.absolute()
os.chdir(PATH)


TOKEN = "801305073078108171"

client=commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Connected')

client.run(TOKEN)


@client.command()
async def balance(ctx):
	await open_account(ctx.author)

	users = await get_bank_data()

	wallet_amt = users[str(user.id)]["wallet"]
	bank_amt = users[str(user.id)]["bank"]

	em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discor.Color.blue())
	em.add_field(name = "Wallet", value = wallet_amt)
	em.add_field(name = "Bank Balance", value = bank_amt)
	await ctx.send(embed = em)



async def bef(ctx):
	await open_account(ctx.author)

	users = await get_bank_data()


	earnings = random.randrange(101)


	await ctx.send(f"Someone gave you {earnings} coins!")


	users[str(user.id)]["wallet"]	+= earnings

	with open(f"{PATH}\\mainbank.json","w") as f:
		json.dump(users,f)


async def open_account(user):

	users = await get_bank_data()


	if str(user.id)	in users:
		return False
	else:
		users[str(user.id)]["wallet"] = 0
		users[str(user.id)]["bank"] = 0

	with open(f"{PATH}\\mainbank.json","w") as f:
		json.dump(users,f)
	return True


async def get_bank_data():
	with open(f"{PATH}\\mainback.json", "w+") as f:
		users = jason.load(f)

	return users

client.run(TOKEN)
