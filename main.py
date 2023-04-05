import azurlane.utils
import discord
from discord.ext import commands
from azurlane.azurapi import AzurAPI

api = AzurAPI()
api.updater.update()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')
ship_name: str
ship = None

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command()
async def help(ctx):
    # Here, you can add the help message for your bot's commands
    help_message = "```List of available commands:\n\n!get_ship <ship_name> - Get ship information by name```"
    await ctx.send(help_message)

@bot.command(name="get_ship")
async def get_ship_by_name(ctx, *discord_text: str):
    global ship
    ship_name = ' '.join(discord_text)
    try:
        ship = api.getShipByName(ship_name)
    except azurlane.utils.UnknownShipException:
        await ctx.send(f"Couldn't find a ship with the name {ship_name}.")
        return

    await getInformation(ctx)

async def getInformation(ctx):
    global ship
    if ship:
        # Create an embed object and set the title, color, and thumbnail
        embed = discord.Embed(title=ship['names']['en'], color=discord.Color.blue())
        embed.set_thumbnail(url=ship['thumbnail'])

        # Add fields for the ship's stats
        embed.add_field(name="Type", value=ship['hullType'], inline=True)
        embed.add_field(name="Nation", value=ship['nationality'], inline=True)
        embed.add_field(name="Rarity", value=ship['rarity'], inline=True)

        # Set the image URL to the full-size image
        image_url = ship['skins'][0]['image']
        embed.set_image(url=image_url)

        # Send the embed
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Couldn't find a ship with the name {ship_name}.")

bot.run('')


