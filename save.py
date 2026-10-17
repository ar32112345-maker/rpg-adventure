import json
import os

SAVE_FILE = "savegame.json"

def save_game(player):
    data = {
        "name": player.name,
        "level": player.level,
        "xp": player.xp,
        "xp_to_next_level": player.xp_to_next_level,
        "hp" : player.hp,
        "max_hp": player.max_hp,
        "attack": player.attack,
        "defense": player.defense,
        "gold": player.gold,
        "crit_chance": player.crit_chance,
        "potions": player.potions,
        "weapon": player.weapon,
        "armor": player.armor,
        "x": player.x,
        "y": player.y,
        "status_effects": player.status_effects,
        "inventory": player.inventory
    }

    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Game saved successfully!")
        return True
    except (OSError, TypeError) as error:
        print(f"Couldn't save the game: {error}")
        return False

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        from player import Player
        player = Player(data["name"])

        attributes = [
            "level", "xp","xp_to_next_level",
            "hp", "maxx_hp", "attack", "defense",
            "crit_chance", "gold", "potions",
            "weapon", "armor", "x", "y",
            "status_effects", "inventory"
        ]
        for attribute in attributes:
            if attribute in data:
                setattr(player, attribute, data[attribute])

        print("Game loaded successfully!")
        return player
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Couldn't load save file: {error}")
        return None
if __name__ == "__main__":
    from player import Player

    player = Player("Hero")
    player.gold = 500
    player.x =3
    player.y =4

    if save_game(player):
        loaded_player = load_game()

        if loaded_player:
            loaded_player.show_stats()
            print(f"Position: ({loaded_player.x}, {loaded_player.y})")
            print(f"Gold: {loaded_player.gold}")