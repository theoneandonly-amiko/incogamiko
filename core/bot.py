# core/bot.py

import disnake
from disnake.ext import commands
import config

# Define intents
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
# This small piece of puzzle will check the outgoing messages to see if it has any keywords included or not.
# If yes, an appropriate response will be given. Bot will not check its own messages, it will only check user messages.
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    for keyword, response in keyword_responses.items():
        if keyword in content:
            await message.channel.send(response)
            break

    await bot.process_commands(message) # "Please don't stop working", Amiko said. 
                                        # In fact, this part will assume if the command still working

# Event: on_ready
# This is a debug message (yes, I called everything "debug") to let you know
# the session for the bot is initialized.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Error handling
# This part will send an error message directly to your current channel if there is someone trying to
# execute a non-existent command.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")
    else:
        await ctx.send("An error occurred.")

# Load initial cogs. Basically load every necessary things. 
# It will give an error to you if failed, too.
initial_extensions = ['base.commands', 'base.rich_presence']

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}: {e}')

# Run the bot with your token
bot.run(config.TOKEN)
