# main.py
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# Core framework engine instantiation configuration matrix mapping
bot = commands.Bot(command_prefix="s", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f"🌟 Termux RPG System Online! Loaded as: {bot.user.name}")
    print(f"👉 Core Prefix Activated: 's' (e.g. scash, sshop, sbattle, shunt)")
    print(f"==================================================")

async def main():
    async with bot:
        # --- MODULAR COG EXPANSION GATEWAYS ---
        # These statements seamlessly bind separate logic scripts at initialization
        await bot.load_extension("economy")
        await bot.load_extension("shop")
        await bot.load_extension("battles")
        await bot.load_extension("hunt")  # ✅ Successfully integrated the hunt file layer
        
        TOKEN = os.getenv("discord_token")
        if TOKEN:
            await bot.start(TOKEN)
        else:
            print("❌ ERROR: 'discord_token' key not detected inside .env configuration file.")

if __name__ == "__main__":
    asyncio.run(main())
  
