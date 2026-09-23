# main.py
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="s", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f"🌟 Termux RPG System Online! Loaded as: {bot.user.name}")
    print(f"👉 Core Prefix Activated: 's' (e.g. scash, sshop, sbattle, scf)")
    print(f"==================================================")

async def main():
    async with bot:
        # Hot-load all Cogs/Modules directly into the framework
        await bot.load_extension("economy")
        await bot.load_extension("shop")
        await bot.load_extension("battles")
        
        TOKEN = os.getenv("discord_token")
        if TOKEN:
            await bot.start(TOKEN)
        else:
            print("❌ ERROR: 'discord_token' key not detected inside .env configuration file.")

if __name__ == "__main__":
    asyncio.run(main())
  
