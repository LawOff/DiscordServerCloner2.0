try:
  import subprocess
  import os
  import sys
  import json
  import time
  import discord
  from utils.cloner import Cloner
  from utils.panel import Panel, Panel_Run
  from discord import Client, Intents
  from rich.prompt import Prompt, Confirm
  from time import sleep
  if discord.__version__ != "1.7.3":
    print("Updating Discord.py...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Discord.py Updated Successfully!")
    print("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)
except Exception:
  print("Installing Requirements...")
  subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
  print("Requirements Installed Successfully!")
  print("Restarting...")
  os.execl(sys.executable, sys.executable, *sys.argv)

client = Client(intents=Intents.all())

with open("./utils/config.json", "r") as json_file:
  data = json.load(json_file)

os.system('cls' if os.name == 'nt' else 'clear')


def clear(option=False):
  sleep(1)
  os.system('cls' if os.name == 'nt' else 'clear')
  if option:
    user = client.user
    guild = client.get_guild(int(INPUT_GUILD_ID))
    Panel_Run(guild, user)
  else:
    Panel()


async def clone_server():
  start_time = time.time()
  guild_from = client.get_guild(int(INPUT_GUILD_ID))
  print(" ")
  guild_to = client.get_guild(await Cloner.guild_create(client, guild_from))
  await Cloner.channels_delete(guild_to)
  if data["copy_settings"]["roles"]:
    await Cloner.roles_create(guild_to, guild_from)
  if data["copy_settings"]["categories"]:
    await Cloner.categories_create(guild_to, guild_from)
  if data["copy_settings"]["channels"]:
    await Cloner.channels_create(guild_to, guild_from)
  if data["copy_settings"]["emojis"]:
    await Cloner.emojis_create(guild_to, guild_from)
  print("\n> Done Cloning Server in " +
        str(round(time.time() - start_time, 2)) + " seconds")


@client.event
async def on_ready():
  clear(True)
  await clone_server()


class ClonerBot:

  def __init__(self):
    self.INPUT_GUILD_ID = None
    with open("./utils/config.json", "r") as json_file:
      self.data = json.load(json_file)

  def clear(self):
    sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    Panel()

  def edit_config(self, option, value, copy_settings=False):
    if copy_settings:
      self.data["copy_settings"][option] = value
    else:
      self.data[option] = value
    with open("./utils/config.json", "w") as json_file:
      json.dump(self.data, json_file, indent=4)

  def edit_settings_function(self):
    print("\nDo you want to copy:")
    categories = Confirm.ask("> Categories?")
    channels = Confirm.ask("> Channels?")
    roles = Confirm.ask("> Roles?")
    emojis = Confirm.ask("> Emojis?")
    for option in ["categories", "channels", "roles", "emojis"]:
      self.edit_config(option, locals()[option], copy_settings=True)

  def main(self):
    self.clear()
    if self.data["token"] == False:
      self.TOKEN = Prompt.ask("\n> Enter your Token")
      sleep(0.5)
    else:
      print("> Token Found")
    self.clear()
    edit_settings = Confirm.ask("\n> Do you want to edit the settings?")
    self.clear()
    if edit_settings:
      self.edit_settings_function()
    self.clear()

    self.INPUT_GUILD_ID = Prompt.ask("\n> Enter the Server ID")
    sleep(0.5)

    return self.INPUT_GUILD_ID, self.TOKEN


if __name__ == "__main__":
  INPUT_GUILD_ID, TOKEN = ClonerBot().main()
  try:
    client.run(TOKEN, bot=False)
    clear()
  except Exception as e:
    print(e)
    print("> Invalid Token")
    data["token"] = False
