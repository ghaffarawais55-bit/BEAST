# hunt.py
import random
import discord
from discord.ext import commands
from config import get_profile, POKEMON_POOL

class HuntEngine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ⏳ Added an economy anti-spam cooldown: 1 use every 15 seconds per user
    @commands.command(name="hunt", aliases=["catch"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def hunt_pokemon(self, ctx):
        """Allows users to search for and catch wild sticker Pokémon. Usage: shunt"""
        prof = get_profile(ctx.author.id)
        
        # Determine encounter rarity tier using weighted probability distribution
        rarity_tier = random.choices(
            ["Common", "Rare", "Legendary", "Mythic"], 
            weights=[0.60, 0.28, 0.10, 0.02]
        )[0]
        
        # Select a random companion profile from the configuration matrix
        wild_pokemon = random.choice(POKEMON_POOL[rarity_tier])
        
        # Base capture rate probabilities
        capture_rates = {
            "Common": 0.75,     # 75% Chance
            "Rare": 0.45,       # 45% Chance
            "Legendary": 0.15,  # 15% Chance
            "Mythic": 0.04      # 4% Chance (Mew/Mewtwo are tough!)
        }
        
        # Generate structural embed UI scene tracking details
        embed = discord.Embed(
            title="🌿 Tall Grass Exploration Encounter!",
            description=f"A wild **[{rarity_tier}] {wild_pokemon['name']}** appeared right in front of you!",
            color=discord.Color.green()
        )
        embed.add_field(name="Encounter Details", value=f"**Species:** {wild_pokemon['name']}\n**HP Capacity:** `{wild_pokemon['hp']}`\n**Base Move:** {wild_pokemon['attack']}")
        
        # Execute absolute capture determination checks
        roll = random.random()
        success_threshold = capture_rates[rarity_tier]
        
        if roll <= success_threshold:
            # Check for existing collection data or init inventory
            if "pokemon" not in prof:
                prof["pokemon"] = []
                
            # Prevent duplicating identical sticker configurations into user data arrays
            already_owned = any(p["name"] == wild_pokemon["name"] for p in prof["pokemon"])
            
            if already_owned:
                # Award consolation currency duplication bounty instead
                bounty = random.randint(5000, 15000)
                prof["sycoizz"] += bounty
                embed.description += f"\n\n✨ You threw a Pokéball and caught it! Since you already owned this sticker, it converted into a duplication credit of `+{bounty:,}` sycoizz!"
                embed.set_footer(text="Wallet balance upgraded successfully.")
            else:
                # Add profile element directly into active runtime collections
                new_capture = {
                    "name": wild_pokemon["name"],
                    "emoji": wild_pokemon["emoji"],
                    "hp": wild_pokemon["hp"],
                    "attack": wild_pokemon["attack"],
                    "equipped_weapon": None
                }
                prof["pokemon"].append(new_capture)
                embed.description += f"\n\n🎉 **SUCCESSFUL CAPTURE!** You threw a Pokéball and caught {wild_pokemon['emoji']} **{wild_pokemon['name']}**! Added directly to your profile inventory loadout."
                embed.set_footer(text="Check your collection using: ssee")
        else:
            embed.description += f"\n\n💨 *Oh no! The wild Pokémon broke out of the ball and fled into deep cover branches...*"
            embed.set_footer(text="Better luck next time! Cooldown active.")

        await ctx.send(embed=embed)

    # Cooldown error response handler interceptor logic
    @hunt_pokemon.error
    async def hunt_error_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ **Slow down!** Your hunting gear is cooling down. Try exploring again in `{error.retry_after:.1f}` seconds.")

async def setup(bot):
    await bot.add_cog(HuntEngine(bot))
  
