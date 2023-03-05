import discord
from colorama import Fore, init, Style
import asyncio
import sys, json

with open("./utils/config.json", "r") as json_file:
  data = json.load(json_file)
  logs_enabled = data["logs"]


def clear_line(n=1):
  LINE_UP = '\033[1A'
  LINE_CLEAR = '\x1b[2K'
  for _ in range(n):
    print(LINE_UP, end=LINE_CLEAR)


def logs(message, type, number=None):
  if logs_enabled:
    log_types = {
      'add': ('[+]', Fore.GREEN),
      'delete': ('[-]', Fore.RED),
      'warning': ('[WARNING]', Fore.YELLOW),
      'error': ('[ERROR]', Fore.RED)
    }
    prefix, color = log_types.get(type, ('[?]', Fore.RESET))

    if number is not None:
      print(f" {color}{prefix}{Style.RESET_ALL} {message}")
    else:
      print(f" {color}{prefix}{Style.RESET_ALL} {message}")
      clear_line()


class Cloner:

  @staticmethod
  async def guild_create(client, guild_from: discord.Guild):
    guild_to = await client.create_guild(guild_from.name)
    try:
      try:
        icon_image = await guild_from.icon_url_as(format='jpg').read()
      except discord.errors.DiscordException:
        logs(f"Can't read icon image from {guild_from.name}", 'error')
        icon_image = None
      await guild_to.edit(name=f'{guild_from.name}')
      if icon_image is not None:
        try:
          await guild_to.edit(icon=icon_image)
          logs(f"Guild Icon Changed: {guild_to.name}", 'add')
        except Exception:
          logs(f"Error While Changing Guild Icon: {guild_to.name}", 'error')
    except discord.Forbidden:
      logs(f"Error While Changing Guild Icon: {guild_to.name}", 'error')
    logs(f"Cloned server: {guild_to.name}", 'add', True)
    return guild_to.id

  @staticmethod
  async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
    roles = [role for role in guild_from.roles if role.name != "@everyone"]
    roles.reverse()
    roles_created = len(roles)
    for role in roles:
      try:
        kwargs = {
          'name': role.name,
          'permissions': role.permissions,
          'colour': role.colour,
          'hoist': role.hoist,
          'mentionable': role.mentionable
        }
        await guild_to.create_role(**kwargs)
        logs(f"Created Role {role.name}", 'add')
      except (discord.Forbidden, discord.HTTPException) as e:
        logs(f"Error creating role {role.name}: {e}", 'error')
    logs(f"Created Roles: {roles_created}", 'add', True)

  @staticmethod
  async def channels_delete(guild_to: discord.Guild):
    channels = guild_to.channels
    channels_deleted = len(channels)
    for channel in channels:
      try:
        await channel.delete()
        logs(f"Deleted Channel: {channel.name}", 'delete')
      except (discord.Forbidden, discord.HTTPException) as e:
        logs(f"Error deleting channel {channel.name}: {e}", 'error')
    logs(f"Deleted Channels: {channels_deleted}", 'delete', True)

  @staticmethod
  async def categories_create(guild_to: discord.Guild,
                              guild_from: discord.Guild):
    channels = guild_from.categories
    for channel in channels:
      try:
        overwrites_to = {
          discord.utils.get(guild_to.roles, name=key.name): value
          for key, value in channel.overwrites.items()
        }
        new_channel = await guild_to.create_category(name=channel.name,
                                                     overwrites=overwrites_to)
        await new_channel.edit(position=channel.position)
        logs(f"Created Category: {channel.name}", 'add')
      except discord.Forbidden:
        logs(f"Error creating category {channel.name}", 'error')
      except discord.HTTPException:
        logs(f"Error creating category {channel.name}", 'error')
    logs(f"Created Categories: {len(channels)}", 'add', True)

  @staticmethod
  async def channels_create(guild_to: discord.Guild,
                            guild_from: discord.Guild):
    channels = guild_from.text_channels + guild_from.voice_channels
    channel_types = {
      discord.TextChannel: guild_to.create_text_channel,
      discord.VoiceChannel: guild_to.create_voice_channel
    }
    channels_created = len(channels)
    for channel in channels:
      await asyncio.sleep(0.2)
      category = discord.utils.get(guild_to.categories,
                                   name=getattr(channel.category, "name",
                                                None))
      overwrites_to = {}
      for key, value in channel.overwrites.items():
        role = discord.utils.get(guild_to.roles, name=key.name)
        overwrites_to[role] = value
      try:
        new_channel = await channel_types[type(channel)
                                          ](name=channel.name,
                                            overwrites=overwrites_to,
                                            position=channel.position)
        if category is not None:
          await new_channel.edit(category=category)
        logs(
          f"Created {'Text' if type(channel) == discord.TextChannel else 'Voice'} Channel: {channel.name}",
          'add')
      except (discord.Forbidden, discord.HTTPException, Exception) as error:
        logs(f"Error While Creating Channel {channel.name}: {error}", 'error')
    logs(f"Created Channels: {channels_created}", 'add', True)

  @staticmethod
  async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
    emoji: discord.Emoji
    emojis_created = len(guild_from.emojis)
    for emoji in guild_from.emojis:
      try:
        await asyncio.sleep(0.2)
        emoji_image = await emoji.url.read()
        await guild_to.create_custom_emoji(name=emoji.name, image=emoji_image)
        logs(f"Created Emoji {emoji.name}", 'add')
      except discord.Forbidden:
        logs(f"Error While Creating Emoji {emoji.name} ", 'error')
      except discord.HTTPException:
        logs(f"Error While Creating Emoji {emoji.name}", 'error')
    logs(f"Created Emojis: {emojis_created}", 'add', True)
