# bot.py
import os

import io
import json
import aiohttp
import requests
import discord
import urllib.parse, urllib.request, re
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
kbx_token = os.getenv('KEEBEX_TOKEN')

#defines bot prefix
bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Whoa there speedy fingers! This command has a 30 second cooldown. Please wait and try again.')
    raise error  # re-raise the error so all the errors will still show up in console
    
#verification command group
@bot.group()
@commands.cooldown (1, 30, commands.BucketType.user)
async def verify(ctx):
    # Connect to Keebex API
    userid = ctx.author.id
    keebex = f"https://keebex.io/api/brilliantdiscord/member/{userid}/invision"
    request = requests.get(keebex, auth=(kbx_token, ''))
    data = request.json()
    kbx_user = data['id']
    kbx_group = data['primaryGroup']['id']
    keebex_upgrade = f"https://www.keebex.io/api/core/members/{kbx_user}?group=7"

    if ctx.invoked_subcommand is None:
        #Formatting for DM
        embed=discord.Embed(
        title="Marketplace Terms and Conditions",
            url="https://keebex.io",
            description="Here are some ways to format text",
            color=discord.Color.blue())
        embed.set_author(name="Keebex", url="https://keebex.io", icon_url="https://content.invisioncic.com/h319081/monthly_2022_02/keebex_discord.png.d900496dc3fd7bf8af90eddc31c8f0b1.png")
        embed.set_thumbnail(url="https://content.invisioncic.com/h319081/monthly_2022_02/keebex_discord.png.d900496dc3fd7bf8af90eddc31c8f0b1.png")
        embed.add_field(name="**1. All Community Rules Apply**", value="Visit the #rules channel to review.", inline=False)
        embed.add_field(name="**2. Shipping**", value="You understand that all shipping responsibility is held by the seller of the Advert. Keebex is only responsible for shipping of official Keebex store items.", inline=False)
        embed.add_field(name="**3. Payment Information**", value="The seller is responsible for providing updated and accurate payment methods. Paypal will always be the suggested method of payment.", inline=False)
        embed.add_field(name="**4. Keebex Responsibilities**", value="Keebex is not responsible for any member-to-member sales. However, Keebex staff are responsible for investigating fraudulent deals. This includes remediation of offending accounts. ", inline=False)
        embed.add_field(name="**5. Accurate Listing Information**", value="It is the responsibility of the seller to maintain accurate listing information meeting all minimum requirements. Adverts that don't present accurate listing information can be hidden or removed.", inline=False)
        embed.add_field(name="**6. Use Good Judgment**", value="If you do not feel comfortable with a deal do **NOT** complete it. Do not hesitate to report the event to staff with details for further investigation.", inline=False)
        embed.add_field(name="**Do you accept?**", value="Please respond with 'accept' (no quotes) if you agree to these terms.", inline=False)
        embed.set_footer(text="Learn more about Keebex here: https://www.keebex.io/articles.html/articles/why-use-keebex-r5/")

        if kbx_group == 7:
            # We don't want to spam embed message, verifying if user is part of Community Members
            print ('User is already verified!')
            await ctx.message.channel.send('You are already verified!')
        else:
            # Yeet
            await ctx.author.send(embed=embed)

@commands.dm_only()
@commands.cooldown (1, 30, commands.BucketType.user)
@verify.command()
async def accept(ctx):
    userid = ctx.author.id
    keebex = f"https://keebex.io/api/brilliantdiscord/member/{userid}/invision"
    request = requests.get(keebex, auth=(kbx_token, ''))
    data = request.json()
    kbx_user = data['id']
    kbx_group = data['primaryGroup']['id']
    keebex_upgrade = f"https://www.keebex.io/api/core/members/{kbx_user}?group=7"
        
    if kbx_group == 7:
        print('User is already verified!')
        await ctx.message.channel.send('You are already verified!')
    else: 
        print ('User is being added to community member group')
        requests.post(keebex_upgrade, auth=(kbx_token, ''), verify=True)
        await ctx.message.channel.send('You are now verified!')
    return kbx_group



bot.run(TOKEN)
