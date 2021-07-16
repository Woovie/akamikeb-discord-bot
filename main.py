from typing import final
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
        match message.content.split():
            # !subnight
            case [command]:
                match command:
                    case "!subnight":
                        sendable = ""
                        name = self.subnight.data["name"]
                        url = self.subnight.data["url"]

                        if len(name) > 0:
                            sendable += f"Subnight is {name}"
                        else:
                            sendable = "No game set <:45:774771310437072954> I guess you're forever alone <:bobK:857020248254578738>"
                        
                        if len(url) > 0:
                            sendable += f"\n{url}"
                        
                        await message.channel.send(sendable)
            # !subnight set <stuff>
            case [command, action, *parameters]:
                match command:
                    case "!subnight":
                        match action:
                            case "set":
                                if message.author.guild_permissions.administrator:
                                    final_payload = {
                                        "name": "",
                                        "url": ""
                                    }
                                    
                                    for partial in parameters:
                                        if partial.startswith("http"):
                                            final_payload["url"] = partial
                                            parameters.remove(partial)
                                    
                                    final_payload["name"] = " ".join(parameters)

                                    self.subnight.set(final_payload)
                                    await self.set_status()

    async def set_status(self):
        if len(self.subnight.data["name"]) > 0:
            status_obj = discord.Game(self.subnight.data["name"])
        else:
            status_obj = discord.Game(config["discord"]["status_placeholder"])
        await client.change_presence(activity=status_obj)

client = DiscordBot()
client.run(config["discord"]["token"])