import discord, json

async def runcode(ctx):
    with open("../embeds/under_construct.json", "r") as help_file:
        embedObj = discord.Embed.from_dict( json.load(help_file)["embed"] )
    await ctx.send(embed=embedObj)
