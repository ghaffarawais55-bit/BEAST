# battles.py
import random
import asyncio
import discord
from discord.ext import commands
from config import get_profile, WEAPONS, POKEMON_POOL, edit_msg_safe

class BattleEngine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="battle")
    async def battle(self, ctx):
        prof = get_profile(ctx.author.id)
        player_pet = prof["pokemon"][0]
        
        bonus_damage = 0
        weapon_title = "None"
        special_strike_action = player_pet["attack"]
        
        if player_pet.get("equipped_weapon"):
            w_meta = WEAPONS[player_pet["equipped_weapon"]]
            bonus_damage = w_meta["dmg"]
            weapon_title = f"{w_meta['name']} [{w_meta['tier']}]"
            special_strike_action = w_meta["attack_name"]

        rarity_tier = random.choices(["Common", "Rare", "Legendary", "Mythic"], weights=[0.55, 0.30, 0.10, 0.05])[0]
        enemy_blueprint = random.choice(POKEMON_POOL[rarity_tier])
        
        p_hp = player_pet["hp"]
        e_hp = enemy_blueprint["hp"]
        e_name = f"Wild {enemy_blueprint['name']}"
        e_emoji = enemy_blueprint["emoji"]

        status_template = (
            "⚔️ **STAGE ENCOUNTER: STICKER COMBAT VECTOR**\n"
            "```\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🔵 {p_emoji} {p_name:<14} HP: [{p_hp:<4}] | Loadout: {w_name}\n"
            "🔴 {e_emoji} {e_name:<14} HP: [{e_hp:<4}] | Tier: {e_tier}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "```\n"
            "**[Log Matrix]:** {log_text}"
        )

        msg = await ctx.send(status_template.format(
            p_emoji=player_pet["emoji"], p_name=player_pet["name"], p_hp=p_hp, w_name=weapon_title,
            e_emoji=e_emoji, e_name=e_name, e_hp=e_hp, e_tier=rarity_tier, log_text="Synchronizing encounter vectors..."
        ))

        while p_hp > 0 and e_hp > 0:
            await asyncio.sleep(1.0)
            
            # --- Player Turn ---
            base_hit = random.randint(15, 30)
            total_p_hit = base_hit + bonus_damage
            e_hp = max(0, e_hp - total_p_hit)
            
            await edit_msg_safe(msg, status_template.format(
                p_emoji=player_pet["emoji"], p_name=player_pet["name"], p_hp=p_hp, w_name=weapon_title,
                e_emoji=e_emoji, e_name=e_name, e_hp=e_hp, e_tier=rarity_tier,
                log_text=f"💥 {player_pet['name']} used {special_strike_action}! Hit {e_name} for {total_p_hit} damage!"
            ))
            
            if e_hp <= 0:
                break
                
            await asyncio.sleep(1.0)
            
            # --- Enemy Turn ---
            enemy_hit = random.randint(12, 28)
            if rarity_tier == "Legendary": enemy_hit += 20
            elif rarity_tier == "Mythic": enemy_hit += 45
                
            p_hp = max(0, p_hp - enemy_hit)
            
            await edit_msg_safe(msg, status_template.format(
                p_emoji=player_pet["emoji"], p_name=player_pet["name"], p_hp=p_hp, w_name=weapon_title,
                e_emoji=e_emoji, e_name=e_name, e_hp=e_hp, e_tier=rarity_tier,
                log_text=f"⚡ {e_name} responds with {enemy_blueprint['attack']}! Dealt {enemy_hit} damage back."
            ))

        await asyncio.sleep(0.8)
        if p_hp > 0:
            if rarity_tier == "Mythic": loot_reward = random.randint(100000, 250000)
            elif rarity_tier == "Legendary": loot_reward = random.randint(40000, 80000)
            else: loot_reward = random.randint(2000, 6000)
            
            prof["sycoizz"] += loot_reward
            final_log = f"🏆 VICTORY! Successfully defeated {e_name}. Collected `+{loot_reward:,}` sycoizz loot payout!"
        else:
            final_log = f"💀 DEFEAT! {player_pet['name']} fainted on the field."

        await edit_msg_safe(msg, status_template.format(
            p_emoji=player_pet["emoji"], p_name=player_pet["name"], p_hp=p_hp, w_name=weapon_title,
            e_emoji=e_emoji, e_name=e_name, e_hp=e_hp, e_tier=rarity_tier, log_text=final_log
        ))

async def setup(bot):
    await bot.add_cog(BattleEngine(bot))
  
