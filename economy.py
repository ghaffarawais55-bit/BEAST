# economy.py
import random
import asyncio
import discord
from discord.ext import commands
from config import get_profile, GEMS, WEAPONS, OWNER_ID, edit_msg_safe

class EconomyEngine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- OWNER-ONLY CORE COMMANDS ---
    @commands.command(name="givecash")
    async def give_cash(self, ctx, target: discord.Member, amount: int):
        if ctx.author.id != OWNER_ID:
            return await ctx.send("❌ Access Denied: This command is restricted to the bot owner only.")
        if amount <= 0:
            return await ctx.send("❌ Amount must be positive.")
        prof = get_profile(target.id)
        prof["sycoizz"] += amount
        await ctx.send(f"👑 **[OWNER ADMIN]** Transferred `{amount:,}` sycoizz into {target.mention}'s account.")

    # --- OWO ECONOMY INTERFACES ---
    @commands.command(name="cash", aliases=["money", "bal"])
    async def cash_cmd(self, ctx, target: discord.Member = None):
        user = target or ctx.author
        prof = get_profile(user.id)
        await ctx.send(f"💳 {user.mention}'s Balance: `{prof['sycoizz']:,}` sycoizz.")

    @commands.command(name="give", aliases=["send", "pay"])
    async def give_cmd(self, ctx, target: discord.Member, amount: int):
        if ctx.author.id == target.id:
            return await ctx.send("❌ You cannot send currency to yourself.")
        if amount <= 0:
            return await ctx.send("❌ Minimum transaction value must clear above 0.")
            
        sender_prof = get_profile(ctx.author.id)
        if sender_prof["sycoizz"] < amount:
            return await ctx.send("❌ Transaction aborted: Insufficient treasury balance.")
            
        receiver_prof = get_profile(target.id)
        sender_prof["sycoizz"] -= amount
        receiver_prof["sycoizz"] += amount
        await ctx.send(f"✅ Successfully transferred `{amount:,}` sycoizz to {target.mention}.")

    @commands.command(name="see", aliases=["profile", "inv", "bag"])
    async def see_cmd(self, ctx, target: discord.Member = None):
        user = target or ctx.author
        prof = get_profile(user.id)
        
        embed = discord.Embed(title=f"🎒 {user.name}'s Adventure Profile Ledger", color=discord.Color.blue())
        embed.add_field(name="💰 Cash Reserves", value=f"`{prof['sycoizz']:,}` sycoizz", inline=True)
        
        gem_display = [GEMS[gid]["name"] for gid in prof["gems"]] if prof["gems"] else ["No gems socketed"]
        embed.add_field(name="💎 Lucky Talismans", value=", ".join(gem_display), inline=True)
        
        pet_lines = []
        for pet in prof["pokemon"]:
            w_eq = f" (⚔️ Equipped: {WEAPONS[pet['equipped_weapon']]['name']})" if pet.get("equipped_weapon") else ""
            pet_lines.append(f"{pet['emoji']} **{pet['name']}** | HP: `{pet['hp']}`{w_eq}")
        
        embed.add_field(name="🐾 Roster Companion Lineup", value="\n".join(pet_lines) if pet_lines else "None", inline=False)
        await ctx.send(embed=embed)

    # --- OWO ANIMATED COINFLIP ---
    @commands.command(name="cf", aliases=["flip"])
    async def coin_flip_gamble(self, ctx, bet: int):
        prof = get_profile(ctx.author.id)
        if bet <= 0 or prof["sycoizz"] < bet:
            return await ctx.send("❌ Invalid currency allocation or bankrupt status parameters.")
            
        luck_modifier = 1.0
        for gid in prof["gems"]:
            if GEMS[gid]["boost"] > luck_modifier:
                luck_modifier = GEMS[gid]["boost"]

        frames = [
            "🪙 **[ OwO FLIPPING ]** ` 🟡 ⟲ SPINNING ⟳ `",
            "🪙 **[ OwO FLIPPING ]** ` ⚪ ⟲ SPINNING ⟳ `",
            "🪙 **[ OwO FLIPPING ]** ` 🟡 ⟲ SPINNING ⟳ `",
            "🪙 **[ OwO FLIPPING ]** ` ⚪ ⟲ SPINNING ⟳ `"
        ]
        
        msg = await ctx.send(frames[0])
        for frame in frames[1:]:
            await asyncio.sleep(0.5)
            await edit_msg_safe(msg, frame)
            
        base_chance = 0.50
        final_chance = base_chance * luck_modifier
        
        await asyncio.sleep(0.4)
        if random.random() <= final_chance:
            prof["sycoizz"] += bet
            await edit_msg_safe(msg, f"🎉 **🎉 HEADS! YOU WIN! 🎉**\n🔥 Luck Factor Activated! Gained `{bet:,}` sycoizz!\n💳 Wallet Total: `{prof['sycoizz']:,}`")
        else:
            prof["sycoizz"] -= bet
            await edit_msg_safe(msg, f"💀 **💀 TAILS! HOUSE WINS! 💀**\nLost `{bet:,}` sycoizz in the void.\n💳 Wallet Total: `{prof['sycoizz']:,}`")

async def setup(bot):
    await bot.add_cog(EconomyEngine(bot))
      
