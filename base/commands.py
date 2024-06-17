# base/commands.py

import disnake
from disnake.ext import commands
import random
import asyncio

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = disnake.Embed(
            title="Bot Commands",
            description="Here's a list of available commands:",
            color=0x7289DA  # Discord color
        )

        for cog, commands_list in mapping.items():
            if cog is None:
                category = "No Category"
            else:
                category = cog.qualified_name

            command_signatures = [self.get_command_signature(cmd) for cmd in commands_list]
            embed.add_field(
                name=category,
                value="\n".join(command_signatures),
                inline=False
            )

        embed.set_footer(text=f"Use {self.context.prefix}help <command> for more info on a command.")
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = disnake.Embed(
            title=f"Command: {command.name}",
            description=command.help or "No description available.",
            color=0x7289DA  # Discord color
        )
        embed.add_field(
            name="Usage",
            value=self.get_command_signature(command),
            inline=False
        )
        await self.get_destination().send(embed=embed)

# Command Definitions
class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hi")
    async def hi(self, ctx):
        """Greets the user."""
        responses = [
            f"Hello, {ctx.author.mention}!",
            "Hi there!",
            "Hey!"
        ]
        await ctx.send(random.choice(responses))

    @commands.command(name="goodbye")
    async def goodbye(self, ctx):
        """Says goodbye to the user."""
        responses = [
            f"Goodbye, {ctx.author.mention}!",
            "See you later!",
            "Bye!"
        ]
        await ctx.send(random.choice(responses))

    @commands.command(name="roll")
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send("Format has to be in NdN!")
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(name="trivia")
    async def trivia(self, ctx):
        """Asks a random trivia question."""
        questions = {
            "What is the capital of France?": ["Paris", "Lyon", "Marseille"],
            "Who wrote 'Hamlet'?": ["William Shakespeare", "Charles Dickens", "Jane Austen"],
            "What is the largest planet in our solar system?": ["Jupiter", "Saturn", "Neptune"]
        }
        question, answers = random.choice(list(questions.items()))
        correct_answer = answers[0]
        random.shuffle(answers)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(f"Trivia Time! {question}\nOptions: {', '.join(answers)}")

        try:
            response = await self.bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            return await ctx.send(f"Sorry, you took too long. The correct answer was {correct_answer}.")

        if response.content.lower() == correct_answer.lower():
            await ctx.send("Correct! 🎉")
        else:
            await ctx.send(f"Wrong! The correct answer was {correct_answer}.")

    @commands.command(name="battle")
    async def battle(self, ctx, user1: disnake.Member, user2: disnake.Member):
        """Initiates a battle between two users."""
        if user1 == user2:
            await ctx.send("You can't battle the same user!")
            return

        player1 = user1
        player2 = user2
        health1 = health2 = 100

        def battle_embed(p1, p2, h1, h2):
            embed = disnake.Embed(title="Battle Time!", color=0xFF5733)
            embed.add_field(name=p1.display_name, value=f"Health: {max(h1, 0)}", inline=True)
            embed.add_field(name=p2.display_name, value=f"Health: {max(h2, 0)}", inline=True)
            embed.set_footer(text="Fight!")
            return embed

        battle_message = await ctx.send(embed=battle_embed(player1, player2, health1, health2))

        while health1 > 0 and health2 > 0:
            turn = random.choice([player1, player2])

            attacker = turn
            defender = player2 if turn == player1 else player1
            damage = random.randint(10, 20)

            if attacker == player1:
                health2 -= damage
            else:
                health1 -= damage

            await battle_message.edit(embed=battle_embed(player1, player2, health1, health2))
            await ctx.send(f"{attacker.display_name} attacks {defender.display_name} for {damage} damage!")
            await asyncio.sleep(2)

        winner = player1 if health1 > 0 else player2
        await ctx.send(f"{winner.display_name} wins the battle!")

def setup(bot):
    bot.add_cog(MyCommands(bot))
    bot.help_command = CustomHelpCommand()
