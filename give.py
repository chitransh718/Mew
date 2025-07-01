# -*- coding: utf-8 -*-
import json
import os
import random
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import ReplyKeyboardMarkup
SAVE_FILE = "players.json"
players = {}

# Starter character image
NOBITA_IMAGE = 'https://i.pinimg.com/736x/85/77/b6/8577b6cc1e0ede4a7777ff5115ab000d.jpg'

# Shop definitions
SHOP_ITEMS = {
    "sword": {"price": 1000, "damage": (8, 9)},
    "gun":   {"price": 2000, "damage": (12, 13)}
}

# Enemy images
enemy_images = {
    'Evil Suneo': 'https://static.wikia.nocookie.net/doraemon/images/7/7f/D24-004.jpg/revision/latest?cb=20161207010551&path-prefix=en',
    'Gian Clone': 'https://i.pinimg.com/736x/f1/17/b4/f117b415de39acab0483b0b3f761b025.jpg',
    'dorapin': 'https://static.wikia.nocookie.net/villains/images/0/08/Dorapin.jpg/revision/latest?cb=20220202082735',
    'Angry Doraemon': 'https://i.pinimg.com/736x/82/47/b1/8247b10fc83141d35ec3849102c75e1f.jpg',
    'mysterious villain': 'https://preview.redd.it/doraemons-most-mysterious-villian-v0-4kmjn96wv8md1.jpg?width=480&format=pjpg&auto=webp&s=eee096e279a8385fdebdbf2999e2ad7dcdd430f1',
    'Evil Nobita': 'https://static.wikia.nocookie.net/doraemon/images/d/d2/D24-003.jpg/revision/latest?cb=20140611054713&path-prefix=en'
}

boss_images = {
    'Demon Underworld': 'https://i.imgur.com/LjcdAB5.png',
    'Space Pirate': 'https://i.imgur.com/bMB0j1B.png',
    'Evil Time Machine': 'https://i.imgur.com/dUclZwT.png',
    'Monster Plant': 'https://i.imgur.com/MR0NSKD.png',
    'Evil Doraemon': 'https://i.imgur.com/Y1acEmf.png'
}

class Player:
    def __init__(self, level=1, max_hp=22, hp=22, attack=None, xp=0, coins=0,
                 nobita_level=1, level_up_cards=0, weapons=None,
                 equipped_weapon=None):
        self.level = level
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack if attack is not None else random.randint(3, 4)
        self.xp = xp
        self.coins = coins
        self.enemy = None
        self.nobita_level = nobita_level
        self.level_up_cards = level_up_cards
        self.weapons = weapons if weapons is not None else []
        self.equipped_weapon = equipped_weapon

    def is_alive(self):
        return self.hp > 0

    def to_dict(self):
        return {
            "level": self.level,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
            "xp": self.xp,
            "coins": self.coins,
            "nobita_level": self.nobita_level,
            "level_up_cards": self.level_up_cards,
            "weapons": self.weapons,
            "equipped_weapon": self.equipped_weapon
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            level=data.get("level", 1),
            max_hp=data.get("max_hp", 22),
            hp=data.get("hp", 22),
            attack=data.get("attack", random.randint(3, 4)),
            xp=data.get("xp", 0),
            coins=data.get("coins", 0),
            nobita_level=data.get("nobita_level", 1),
            level_up_cards=data.get("level_up_cards", 0),
            weapons=data.get("weapons", []),
            equipped_weapon=data.get("equipped_weapon")
        )

class Enemy:
    def __init__(self):
        BOSS_SPAWN_RATE = 0.001  # ~0.1% chance
        self.is_boss = random.random() < BOSS_SPAWN_RATE
        if self.is_boss:
            self.name = random.choice(list(boss_images.keys()))
            self.image = boss_images[self.name]
            base_hp = random.randint(60, 100)
            self.max_hp = int(base_hp * random.uniform(2.0, 2.5))
            self.attack = random.randint(20, 35)
        else:
            self.name = random.choice(list(enemy_images.keys()))
            self.image = enemy_images[self.name]
            self.max_hp = random.randint(20, 60)
            self.attack = random.randint(5, 15)
        self.hp = self.max_hp

    def is_alive(self):
        return self.hp > 0

def save_players():
    with open(SAVE_FILE, "w") as f:
        json.dump({uid: p.to_dict() for uid, p in players.items()}, f)

def load_players():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return {int(uid): Player.from_dict(pdata) for uid, pdata in data.items()}
    return {}

def get_hp_bar(current, total, length=10):
    current = max(0, min(current, total))
    filled = int(length * current / total)
    empty = length - filled
    return "[" + "" * filled + "" * empty + f"] {current}/{total}"

def get_required_xp(level):
    return level * 5000

#  Bot Commands 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        players[user_id] = Player()
        save_players()
        await update.message.reply_photo(
            photo=NOBITA_IMAGE,
            caption=" Congratulations! You got *Nobita* as your starter character!\nLet's begin your Doraemon adventure!",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(" You have already started your journey!")

    #  Yeh part explore button dikhayega
    keyboard = [["/explore"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(" Tap to explore!", reply_markup=reply_markup)

async def explore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if not player:
        player = Player()
        players[user_id] = player
    if player.hp <= 0:
        player.hp = player.max_hp
    enemy = Enemy()
    player.enemy = enemy
    save_players()
    keyboard = [[InlineKeyboardButton(" Fight", callback_data="fight_start")]]
    await update.message.reply_photo(photo=enemy.image,
                                     caption=f" A wild {enemy.name} appeared! HP: {enemy.hp}/{enemy.max_hp}",
                                     reply_markup=InlineKeyboardMarkup(keyboard))

async def fight_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    player = players.get(user_id)
    if not player or not player.enemy:
        await query.edit_message_caption(" No enemy found.")
        return
    enemy = player.enemy
    enemy_bar = get_hp_bar(enemy.hp, enemy.max_hp)
    player_bar = get_hp_bar(player.hp, player.max_hp)
    if player.equipped_weapon:
        btn_label = f"Use {player.equipped_weapon.title()}"
        cb_data = "weapon_attack"
    else:
        btn_label = "Attack"
        cb_data = "attack"
    keyboard = [[InlineKeyboardButton(f" {btn_label}", callback_data=cb_data),
                 InlineKeyboardButton(" Escape", callback_data="escape")]]
    await query.edit_message_caption(
        caption=f" What will you do?\n {enemy.name} HP: {enemy_bar}\n You HP:     {player_bar}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def _weapon_attack(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    player = players.get(user_id)
    if not player or not player.enemy:
        await query.edit_message_text(" No enemy to attack.")
        return

    enemy = player.enemy

    # Attack damage calculation
    if player.equipped_weapon in SHOP_ITEMS:
        dmg = random.randint(*SHOP_ITEMS[player.equipped_weapon]['damage'])
        weapon_used = player.equipped_weapon.title()
    else:
        dmg = player.attack
        weapon_used = "Fist"

    enemy.hp -= dmg
    result = f" You used {weapon_used} and dealt {dmg} damage to {enemy.name}.\n"

    if enemy.is_alive():
        # Enemy hits back
        player.hp -= enemy.attack
        result += f" The {enemy.name} hits you for {enemy.attack} damage.\n"

        # Faint check right after enemy hits
        if player.hp <= 0:
            result += "\n You fainted!"
            player.enemy = None
            player.hp = player.max_hp
            save_players()
            await query.edit_message_caption(caption=result)
            return

        enemy_bar = get_hp_bar(enemy.hp, enemy.max_hp)
        player_bar = get_hp_bar(player.hp, player.max_hp)
        result += f" {enemy.name} HP: {enemy_bar}\n You HP:     {player_bar}"

        # Fight buttons
        btn_label = f"Use {weapon_used}" if player.equipped_weapon else "Attack"
        cb = "weapon_attack" if player.equipped_weapon else "attack"
        kb = [[
            InlineKeyboardButton(f" {btn_label}", callback_data=cb),
            InlineKeyboardButton(" Escape", callback_data="escape")
        ]]
        await query.edit_message_caption(caption=result, reply_markup=InlineKeyboardMarkup(kb))
    else:
        # Enemy defeated
        xp = random.randint(500, 1000) if enemy.is_boss else random.randint(100, 160)
        coins = random.randint(800, 1000) if enemy.is_boss else random.randint(70, 120)
        card = 1 if (enemy.is_boss or random.random() < 0.03) else 0

        result += f" You defeated {enemy.name}! Gained {xp} XP and {coins} coins."
        if card:
            player.level_up_cards += 1
            result += "\\n You found a Level-Up Card!"

        player.xp += xp
        player.coins += coins
        player.enemy = None
        save_players()
        await query.edit_message_caption(caption=result)

async def attack_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _weapon_attack(update, context)

async def weapon_attack_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _weapon_attack(update, context)

async def escape_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    player = players.get(user_id)
    if player: player.enemy = None; save_players()
    await query.edit_message_caption(" You ran away!")

async def use_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if not player:
        await update.message.reply_text("Please /start first.")
        return
    if player.level_up_cards > 0:
        player.level_up_cards -= 1; player.nobita_level += 1; save_players()
        await update.message.reply_text(f" Nobita leveled up to level {player.nobita_level}!")
    else:
        await update.message.reply_text(" You don't have any Level-Up Cards.")

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " *Shop Items:*\n"
    icon_map = {"sword": "", "gun": ""}
    for name, item in SHOP_ITEMS.items():
        emoji = icon_map.get(name, "")
        damage_range = f"{item['damage'][0]}-{item['damage'][1]}"
        msg += f"- {emoji} *{name.title()}* - {item['price']} coins (Damage: {damage_range})\n"
    msg += "\nUse `/buy <item_name>` to purchase."
    await update.message.reply_text(msg, parse_mode="Markdown")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id; player = players.get(user_id)
    if not player:
        await update.message.reply_text("Please /start first.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /buy <item_name>")
        return
    name = context.args[0].lower(); item = SHOP_ITEMS.get(name)
    if not item:
        await update.message.reply_text(" Item not found.")
        return
    if name in player.weapons:
        await update.message.reply_text(f" You already own {name}.")
        return
    if player.coins < item['price']:
        await update.message.reply_text(" Not enough coins.")
        return
    player.coins -= item['price']
    player.weapons.append(name)
    save_players()
    await update.message.reply_text(f" You bought {name.title()}!")

async def equip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id; player = players.get(user_id)
    if not player:
        await update.message.reply_text("Please /start first.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /equip <item_name>")
        return
    name = context.args[0].lower()
    if name not in player.weapons:
        await update.message.reply_text(f" You don't own {name}.")
        return
    player.equipped_weapon = name
    save_players()
    await update.message.reply_text(f" Equipped {name.title()}.")

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id; player = players.get(user_id)
    if not player:
        await update.message.reply_text("Please /start first.")
        return
    msg = " *Inventory*\n"
    msg += f"-  *Coins:* {player.coins}\n"
    if player.weapons:
        weapons_list = ', '.join(w.title() for w in player.weapons)
    else:
        weapons_list = "None"
    msg += f"-  *Weapons:* {weapons_list}\n"
    if player.equipped_weapon:
        msg += f"-  *Equipped:* {player.equipped_weapon.title()}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def mystats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if not player:
        await update.message.reply_text("Please /start first.")
        return
    xp = player.xp
    user_level = xp // 5000
    msg = " *My Stats*\n"
    msg += f" *User ID:* `{user_id}`\n"
    msg += f" *XP:* {player.xp}\n"
    msg += f" *User Level:* {user_level}\n"
    msg += f" *Characters Owned:* 1"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if not player:
        await update.message.reply_text("Please /start first.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /stats <character_name>")
        return
    name = context.args[0].lower()
    if name == "nobita":
        caption = "*Nobita's Stats:*\n"
        caption += f" Level: {player.nobita_level}\n"
        caption += f" Attack: {player.attack}\n"
        caption += f" HP: {player.hp}/{player.max_hp}\n"
        caption += f"User ID: `{user_id}`"
        await update.message.reply_photo(photo=NOBITA_IMAGE, caption=caption, parse_mode="Markdown")
    else:
        await update.message.reply_text(" Character not found.")

async def main():
    global players
    players = load_players()
    TOKEN = os.getenv("TOKEN")
    print(f"TOKEN loaded? {'Yes' if TOKEN else 'No'}")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("explore", explore))
    app.add_handler(CallbackQueryHandler(fight_start_callback, pattern="fight_start"))
    app.add_handler(CallbackQueryHandler(attack_callback, pattern="attack"))
    app.add_handler(CallbackQueryHandler(weapon_attack_callback, pattern="weapon_attack"))
    app.add_handler(CallbackQueryHandler(escape_callback, pattern="escape"))
    app.add_handler(CommandHandler("use_card", use_card))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("equip", equip))
    app.add_handler(CommandHandler("inventory", inventory))
    app.add_handler(CommandHandler("mystats", mystats))
    app.add_handler(CommandHandler("stats", stats))
    print("Bot is running...")
    print("Initializing bot...")
    await app.run_polling()
