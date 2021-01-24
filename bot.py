from discord.ext import commands
import random, pathlib, os, json, discord, base64

path = pathlib.Path(__file__).parent.absolute()
os.chdir(path)

TOKEN = ""
with open("config.txt", "r") as f:
    TOKEN = base64.b64decode(bytes(f.read().strip(), "utf-8")).decode('utf-8')

client = commands.Bot(command_prefix = '$')

botObj =  commands.Bot(command_prefix="$", help_command=None)

@client.event
async def on_ready():
	print('Connected')

@botObj.command(aliases=["h"])
async def help(ctx):
	await bot_help.help(ctx)


@client.command(aliases = ["bal"])
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


@client.command(aliases = ["with"])
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



@client.command(aliases = ["dep"])
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


@client.command(aliases = ["r"])
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


@client.command(aliases = ["s"])
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

	await update_bank(ctx.author,-1*amount,'wallet')
	await update_bank(member,amount,"wallet")

	await ctx.send(f"You gave {amount} coins!")


@client.command(aliases = ["sl"])
async def slots(ctx,amount = None):
	await open_account(ctx.author)

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[0]:
		await ctx.send("You don't have that much money!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	final = [random.choice([":seven:",":rock:",":flame:",":ocean:",":poop:",":expressionless:",":money_mouth:"]) for i in range(3)]

	await ctx.send(str(final))

	if final.count(final[0]) == 3:
		await update_bank(ctx.author,2*amount)
		await ctx.send("You won! :D")
	else:
		await update_bank(ctx.author,-1*amount)
		await ctx.send("You Lost!:C")

#async def jackpot(amount = 0,mode = "pool"):
#		if final.count(final[0]) == 5:
#	    await update_bank(ctx.author,2*amount) in users
#	    return False
#
#	else:
#		with open("pool.json", "w") as file:
#			users[str(amount)]["jackpot"] = amount
#			jackpot = json.load(file)["wallet"]
#			jackpot += amount
#			json.dump(jackpot, file)
#
#	with open("pool.json","w") as f:
#		json.dump(users,f)
#	return True

	if amount == None:
		await ctx.send('Please enter the amount you want to withdraw')
		return


mainshop = [#{"name":"Dildo","price":69,"description":":eggplant:Very Popular among the Ladies"},
			#{"name":"Electric Vibrator","price":420,"description":":magic_wand:Even more Popular among the Ladies"},
			{"name":"Watch","price":200,"description":":watch:Tells Time Very Well :laughing:"},
			{"name":"Laptop","price":1000,"description":":computer:Good for work. :+1:"},
			{"name":"PC","price":5000,"description":":desktop:Gamers only :sunglasses:"},
			{"name":"House","price":20000,"description":":house:You know what they say, there is no place like home, but home, so pls just buy it..... pls...."}]

@client.command(aliases = ["Shop"])
async def shop(ctx):
	em = discord.Embed(title = "Shop")

	for item in mainshop:
		name = item["name"]
		price = item["price"]
		desc = item["description"]
		em.add_field(name = name, value = f"${price} | {desc}")

	await ctx.send(embed = em)



@client.command()
async def buy(ctx, item, amount = 1):
	await open_account(ctx.author)

	res = await buy_this(ctx.author,item,amount)

	if not res[0]:
		if res[1]==1:
			await ctx.send("That Object Isn't there!")
			return
		if res[1]==2:
			await ctx.send(f"You don't have enough in your wallet to buy this Item")
			return

	await ctx.send(f"You just bought {item} for {amount} coins!")

@client.command(aliases = ["inv"])
async def inventory(ctx):
	await open_account(ctx.author)
	user = ctx.author
	users = await get_bank_data()

	try:
		inventory = users[str(user.id)]["inventory"]
	except:
		inventory = []


	em = discord.Embed(title = "inventory")
	for item in inventory:
		name = item["item"]
		amount = item["amount"]

		em.add_field(name = name, value = amount)

	await ctx.send(embed = em)

async def buy_this(user,item_name,amount):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			if price==None:
				price = item["price"]
			break

	if name_ == None:
		return [False,1]

	cost = price*amount

	user = await get_bank_data()

	bal = await update_bank(user)



	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["inventory"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt - amount
				if new_amt < 0:
					return [False,2]
				user[str(user.id)]["inventory"][index]["amount"] = new_amt
				t = 1
				break
			index+=1
		if t == None:
			return [False,3]
	except:
		return [False,3]

	with open("mainbank.json","w") as f:
		json.dump(user,f)

	await update_bank(user,cost,"wallet")

	return[True,"Worked"]

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your inventory.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your inventory.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

#@client.command(aliases = ["lb", "leaderboard"])
#async def leaderboard(ctx,top = 1):
#	users = await get_bank_data()
#	netWorth = lambda user: users[user]["wallet"] + users[user]["bank"]
#	leader_board = {NetWort(user): int(user) for user in users[:top]}
#
#	embedObj = discord.Embed(
#		title = f"Top { top } Richest People",
#		description = "This is decided on the basis of raw money in the bank and wallet",
#		color = discord.Color(0xfa43ee)
#		)
#
#	counter = 0
#	worths = sorted(list(leader_board.keys()))[::-1]
#	names = sorted(list(leader_board.values()))[::-1]
#
#	for i, j in zip(worths, names):
#		username = client.get_user( j ).name
#
#		embedObj.add_field(
#			name   = f"{ counter }. { username }",
#			value  = f"{ i }",
#			inline = False)

#		counter += 1

#	await ctx.send(embed = embedObj)

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
