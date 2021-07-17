from typing import Optional
from discord import Client, Message, channel, Game
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_permission, create_option
from discord_slash.model import SlashCommandPermissionType
import configparser, subnight, random

config = configparser.ConfigParser()
config.read("config.ini")

command_prefix = config['discord']['prefix']

class DiscordBot(Client):
    async def on_ready(self):
        self.subnight = subnight.Subnight()
        await self.set_status()
        print("Bot is ready")

    async def on_message(self, message: Message):
        if isinstance(message.channel, channel.TextChannel):
            await self.handle_subnight(message)

    async def handle_subnight(self, message):
        match message.content.split():
            case [command]:
                match command:
                    case "!subnight":
                        result = await self.create_subnight_message()
                        await message.channel.send(result)

            case [command, action, *parameters]:
                match command:
                    case "!subnight":
                        match action:
                            case "set":
                                if message.author.guild_permissions.administrator:
                                    result = subnight.create_subnight_payload(parameters)
                                    self.subnight.set(result)
                                    await self.set_status()

    async def create_subnight_message(self):
        sendable = ""
        name = self.subnight.data["name"]
        url = self.subnight.data["url"]

        if len(name) > 0:
            sendable += f"Subnight is {name}"
        else:
            sendable = "No game set <:45:774771310437072954> I guess you're forever alone <:bobK:857020248254578738>"
        
        if len(url) > 0:
            sendable += f"\n{url}"
        
        return sendable

    async def set_status(self):
        if len(self.subnight.data["name"]) > 0:
            status_obj = Game(self.subnight.data["name"])
        else:
            status_obj = Game(config["discord"]["status_placeholder"])
        await client.change_presence(activity=status_obj)

client = DiscordBot()
slash = SlashCommand(client=client, sync_commands=True)

mike_guild = [105420838487990272]# Only allow on akamikeb's discord
all_guild = [105420838487990272, 454065561903562773]# Other ID is my private server

mod_only_permissions = {
    105420838487990272: [
        create_permission(105423928192688128, SlashCommandPermissionType.ROLE, True),# Moderator role
        create_permission(105420838487990272, SlashCommandPermissionType.ROLE, False)# @everyone role
    ]
}

@slash.subcommand(
    base="admin",
    subcommand_group="subnight",
    name="set",
    description="Set subnight information",
    guild_ids=mike_guild,
    options=[
        create_option(
            name="name",
            description="Name of the game",
            option_type=3,
            required=True
        ),
        create_option(
            name="url",
            description="URL to include",
            option_type=3,
            required=False
        )
    ],
    base_description="Moderator only commands",
    base_default_permission=False,
    base_permissions=mod_only_permissions
)
async def subnight_set(context: SlashContext, name: str, url: Optional[str]):
    await context.send(f"{name}")

@slash.subcommand(
    base="everyone",
    subcommand_group="subnight",
    name="get",
    description="Get subnight information",
    guild_ids=mike_guild,
    base_description="Commands anyone can run",
    base_default_permission=True
)
async def subnight_get(context: SlashContext):
    await context.send(f"aaAAaaaA")

@slash.subcommand(
    base="everyone",
    subcommand_group="fun",
    name="bark",
    description="woof",
    guild_ids=all_guild,
)
async def woof(context: SlashContext):
    barks = [
        "woof",
        "*woof*",
        "**woof**",
        "BORK",
        "bark bark",
        "\*heavy breathing\*",
        "butter dog the dog with the butter butter dog dog with the butter on him the dog with the butter butter dog"
    ]
    await context.send(barks[random.randint(0, len(barks)-1)])

client.run(config["discord"]["token"])