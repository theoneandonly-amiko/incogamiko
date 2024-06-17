# base/rich_presence.py

import disnake
from disnake.ext import commands, tasks
import aiohttp
import random
import config

class YouTubePresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_presence.start()

    def cog_unload(self):
        self.update_presence.cancel()

    @tasks.loop(minutes=5)
    async def update_presence(self):
        async with aiohttp.ClientSession() as session:
            url = f"https://www.googleapis.com/youtube/v3/search?channelId={config.YOUTUBE_CHANNEL_ID}&part=snippet&type=video&maxResults=50&key={config.YOUTUBE_API_KEY}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'items' in data and len(data['items']) > 0:
                        video = random.choice(data['items'])
                        video_title = video['snippet']['title']
                        video_id = video['id']['videoId']
                        await self.bot.change_presence(
                            activity=disnake.Activity(
                                type=disnake.ActivityType.watching,
                                name=f"{video_title} on YouTube",
                                url=f"https://www.youtube.com/watch?v={video_id}"
                            )
                        )

    @update_presence.before_loop
    async def before_update_presence(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(YouTubePresence(bot))
