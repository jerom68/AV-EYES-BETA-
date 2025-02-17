import discord
import os
import random
import requests
from discord.ext import commands
from flask import Flask

# Enable intents for commands to work
intents = discord.Intents.default()
intents.message_content = True  # Important for message-based commands

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents)

# Flask app for Render port binding
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Command: Check bot latency
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert to ms
    await ctx.send(f'🏓 Pong! Latency: {latency}ms')

# Command: Send a random joke
@bot.command()
async def joke(ctx):
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
        "Why don’t programmers like nature? It has too many bugs."
    ]
    await ctx.send(random.choice(jokes))

# Command: Send a random fun fact
@bot.command()
async def fact(ctx):
    facts = [
        "Honey never spoils.",
        "Bananas are berries, but strawberries are not.",
        "There are more stars in the universe than grains of sand on all the Earth's beaches."
    ]
    await ctx.send(random.choice(facts))

# Command: Get a random waifu image
@bot.command()
async def waifu(ctx):
    response = requests.get('https://api.waifu.pics/sfw/waifu')
    img_url = response.json()['url']
    await ctx.send(img_url)

# Command: Get a random neko image
@bot.command()
async def neko(ctx):
    response = requests.get('https://api.waifu.pics/sfw/neko')
    img_url = response.json()['url']
    await ctx.send(img_url)

# Command: Get a random anime GIF
@bot.command()
async def anigif(ctx):
    response = requests.get('https://api.waifu.pics/sfw/waifu')  # Anime GIF API unavailable, using waifu API instead
    img_url = response.json()['url']
    await ctx.send(img_url)

# Command: Play Rock, Paper, Scissors
@bot.command()
async def rps(ctx, choice: str):
    rps_choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(rps_choices)
    
    if choice.lower() not in rps_choices:
        await ctx.send("Please choose rock, paper, or scissors!")
        return

    result = ""
    if choice.lower() == bot_choice:
        result = "It's a tie!"
    elif (choice.lower() == "rock" and bot_choice == "scissors") or \
         (choice.lower() == "paper" and bot_choice == "rock") or \
         (choice.lower() == "scissors" and bot_choice == "paper"):
        result = "You win! 🎉"
    else:
        result = "I win! 😈"

    await ctx.send(f"You chose **{choice}**. I chose **{bot_choice}**. {result}")

# Event: When bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the Flask app and bot
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Get port from Render
    app.run(host="0.0.0.0", port=port)  # Start Flask app
    
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # Start bot
