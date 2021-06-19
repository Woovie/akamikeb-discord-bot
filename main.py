import discord, configparser, subnight

config = configparser.ConfigParser()
config.read("config.ini")

command_prefix = config['discord']['prefix']

class DiscordBot(discord.Client):
    async def on_ready(self):
        current_game = subnight.Subnight().get()
        if current_game == "":
            current_game = "bored and lonely"
        await self.set_status(current_game)
        print("Bot is ready")

    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.channel.TextChannel):
            if message.content.startswith(f"{command_prefix}subnight"):
                await self.handle_subnight(message)
            #elif message.content.startswith(f"{command_prefix}notifications"):

    async def handle_subnight(self, message):
        msgsplit = message.content.split()
        if message.content == f"{command_prefix}subnight" or message.content == f"{command_prefix}subnight get":
            game_information = subnight.Subnight().get()
            game_info_message = "No game set presently. Some of you may die, but that's a risk I'm willing to take."
            if len(game_information) > 1:
                game_information_split = game_information.split("\n")
                game_info_message = f"Subnight game is {game_information_split[0]}" if len(game_information_split[1]) < 5 else f"Subnight game is {game_information_split[0]}\nURL: {game_information_split[1]}"
            await message.channel.send(game_info_message)
        elif len(msgsplit) > 1 and message.content != "{command_prefix}subnight get":
            if msgsplit[1] == "set":
                if message.author.guild_permissions.administrator:
                    game_url = ""
                    game_name = ""
                    for line in msgsplit:
                        if line.startswith("http"):
                            game_url = line
                            msgsplit.remove(line)
                    game_name = " ".join(msgsplit[2:])
                    result = subnight.Subnight().set(f"{game_name}\n{game_url}")
                    if game_name == "" or game_name == " ":
                        game_name = "bored and lonely"
                    await self.set_status(game_name)
                    await message.channel.send(f"Attempted setting game, result is: {result}")

    async def configure_notifications(self, message):
        pass

    async def handle_notifications(self, message):
        pass

    async def new_youtube_video(self):
        pass

    async def twitch_live(self):
        pass

    async def set_status(self, status: str):
         status_obj = discord.Game(status)
         await client.change_presence(activity=status_obj)

client = DiscordBot()
client.run(config["discord"]["token"])
