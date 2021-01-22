import discord
from discord.ext import commands
import json
import os
import random
import pathlib

path = pathlib.Path(__file__).parent.absolute()
os.chdir(path)

TOKEN = 'ODAxMzA1MDczMDc4MTA4MTcx.YAevgA.Wfkh2EeuzvI48vkYzd1KIPeFaMY'

client = commands.Bot(command_prefix = 't.')

@client.event
async def on_ready():
    print('Connected')
    

@client.command()
async def balance(ctx):
	await open_account(ctx.author)
	user = ctx.author
	users = await get_bank_data()

	wallet_amt = users[str(user.id)]["wallet"]
	bank_amt = users[str(user.id)]["bank"]

	em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.red())
	em.add_field(name = "Wallet balance", value = wallet_amt)
	em.add_field(name = "Bank balance", value = bank_amt)
	await ctx.send(embed = em)


@client.command()
async def beg(ctx):
	await open_account(ctx.author)

	users = await get_bank_data()

	user = ctx.author
	
	earnings = random.randrange(101)


	await ctx.send(f"Someone gave you {earnings} coins!")


	users[str(user.id)]["wallet"]	+= earnings

	with open("mainbank.json","w") as f:
		json.dump(users,f)


@client.command()
async def withdraw(ctx,amount = None):
	await open_account(ctx.author)
	if amount == 'all':
		amount = bal[0]

	if amount == None:
		await ctx.send('Please enter the amount you want to withdraw')
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[1]:
		await ctx.send("You don't have that much money!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author,amount)	
	await update_bank(ctx.author,-1*amount,"bank")	

	await ctx.send(f"You withdrew {amount} coins!")



@client.command()
async def deposit(ctx,amount = None):
	await open_account(ctx.author)
	if amount == 'all':
		amount = bal[1]


	if amount == None:
		await ctx.send('Please enter the amount you want to withdraw')
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[0]:
		await ctx.send("You don't have that much money!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author,-1*amount)	
	await update_bank(ctx.author,amount,"bank")	

	await ctx.send(f"You deposited {amount} coins!")


@client.command()
async def rob(ctx,member:discord.Member):
	await open_account(ctx.author)
	await open_account(member)

	bal = await update_bank(member)

	if bal[0]<100:
		await ctx.send("Not worth it, Mate!")
		return

	earnings = random.randrange(0,bal[0])

	await update_bank(ctx.author,earnings,'wallet')	
	await update_bank(member,-1*earnings)	

	await ctx.send(f"You robbed {member} and got {earnings} coins!")	


@client.command()
async def send(ctx,member:discord.Member,amount = None):
	await open_account(ctx.author)
	await open_account(member)
	if amount == 'all':
		amount = bal[0]


	if amount == None:
		await ctx.send('Please enter the amount you want to withdraw')
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[1]:
		await ctx.send("You don't have that much money!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author,-1*amount,'bank')	
	await update_bank(member,amount,"bank")	

	await ctx.send(f"You gave {amount} coins!")	


@client.command()
async def slots(ctx,amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send('Please enter the amount you want to withdraw')
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[0]:
		await ctx.send("You don't have that much money!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	final =[]	
	for i in range(3):
		a = random.choice(["7","8","9"])

		final.append(a)

	await ctx.send(str(final))

	if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
		await update_bank(ctx.author,2*amount)	
		await ctx.send("You won! :D")
	else:
		await update_bank(ctx.author,-1*amount)	
		await ctx.send("You Lost!:C")


async def open_account(user):

	users = await get_bank_data()


	if str(user.id)	in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["wallet"] = 250
		users[str(user.id)]["bank"] = 0

	with open("mainbank.json","w") as f:
		json.dump(users,f)
	return True



async def get_bank_data():
	with open("mainbank.json","r") as f:
		users = json.load(f)

	return users	


async def update_bank(user,change = 0,mode = 'wallet'):
	users = await get_bank_data()

	users[str(user.id)][mode] += change

	with open("mainbank.json","w") as f:
		json.dump(users,f)

	bal = [users[str(user.id)]['wallet'],users[str(user.id)]['bank']]	
	return bal	
















while True:
  client.run(TOKEN)





