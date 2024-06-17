# core/bot.py

import disnake
from disnake.ext import commands
import config

# Define intents explicitly
intents = disnake.Intents.all()

# Initialize the bot with intents and the prefix from config
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Define keywords and responses (sample data)
keyword_responses = {
    "hello": "Hi there!",
    "bye": "Goodbye!",
    "python": "Python is awesome!"
    # Add more keywords and responses as needed
}

# Event: on_message
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    for keyword, response in keyword_responses.items():
        if keyword in content:
            await message.channel.send(response)
            break

    await bot.process_commands(message)

# Event: on_ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")
    else:
        await ctx.send("An error occurred.")

# Load initial cogs
initial_extensions = ['base.commands', 'base.rich_presence']

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}: {e}')

# Run the bot with your token
bot.run(config.TOKEN)
