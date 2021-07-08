import discord, configparser, subnight

config = configparser.ConfigParser()
config.read("config.ini")

command_prefix = config['discord']['prefix']

class DiscordBot(discord.Client):
    async def on_ready(self):
        self.subnight = subnight.Subnight()
        await self.set_status()
        print("Bot is ready")

    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.channel.TextChannel):
            if message.content.startswith(f"{command_prefix}subnight"):
                await self.handle_subnight(message)

    async def handle_subnight(self, message):
        if message.content == f"{command_prefix}subnight" or message.content == f"{command_prefix}subnight get":
            name = self.subnight.data["name"]
            url = self.subnight.data["url"]
            if len(name) > 0:
                await message.channel.send(f"Subnight is {name}."+"\n"+f"URL: {url}")
            else:
                await message.channel.send("No game set <:45:774771310437072954> I guess you're forever alone <:bobK:857020248254578738>")
        elif message.content.startswith(f"{command_prefix}subnight set"):
            if message.author.guild_permissions.administrator:
                msgsplit = message.content.split(' ')
                if len(msgsplit) > 2:
                    for line in msgsplit:
                        if line.startswith("http"):
                            game_url = line
                            msgsplit.remove(line)
                    game_name = " ".join(msgsplit[2:])
                    result = self.subnight.set({
                      "name": game_name,
                      "url": game_url
                    })
                    await self.set_status()
                else:
                    self.subnight.set({
                        "name": "",
                        "url": ""
                    })
                    await self.set_status()

    async def set_status(self):
        if len(self.subnight.data["name"]) > 0:
            status_obj = discord.Game(self.subnight.data["name"])
        else:
            status_obj = discord.Game(config['discord']['status_placeholder'])
        await client.change_presence(activity=status_obj)

client = DiscordBot()
client.run(config["discord"]["token"])
