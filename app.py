
import streamlit as st
import random

from player import Player
from enemy import create_goblin, create_wolf, create_orc
from map import GameMap
from save import save_game, load_game

st.set_page_config(
    page_title="RPG Adventure",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ My RPG Adventure")
st.caption("Explore. Fight. Collect. Survive.")

# ---------- INITIALIZE GAME ----------
if "player" not in st.session_state:
    st.session_state.player = Player("Hero")

if "game_map" not in st.session_state:
    st.session_state.game_map = GameMap()

if "enemy" not in st.session_state:
    st.session_state.enemy = None

if "battle_log" not in st.session_state:
    st.session_state.battle_log = []

if "message" not in st.session_state:
    st.session_state.message = "Your adventure begins!"

player = st.session_state.player
game_map = st.session_state.game_map


def add_log(message):
    st.session_state.battle_log.append(message)
    st.session_state.battle_log = st.session_state.battle_log[-12:]


def start_battle(enemy):
    st.session_state.enemy = enemy
    st.session_state.battle_log = [
        f"A wild {enemy.name} appeared!"
    ]


def finish_battle(enemy):
    player.gold += enemy.gold_reward
    player.gain_xp(enemy.xp_reward)
    add_log(
        f"Victory! +{enemy.xp_reward} XP, "
        f"+{enemy.gold_reward} Gold."
    )
    st.session_state.enemy = None


# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("🧙 Character")
    st.write(f"**Name:** {player.name}")
    st.progress(
        max(0.0, min(1.0, player.hp / player.max_hp)),
        text=f"HP: {player.hp}/{player.max_hp}"
    )
    st.write(f"**Level:** {player.level}")
    st.write(f"**XP:** {player.xp}/{player.xp_to_next_level}")
    st.write(f"**Attack:** {player.attack}")
    st.write(f"**Defense:** {player.defense}")
    st.write(f"**Gold:** {player.gold}")
    st.write(f"**Potions:** {player.potions}")

    st.divider()

    if st.button("💾 Save Game", use_container_width=True):
        save_game(player)
        st.success("Game saved!")

    if st.button("📂 Load Game", use_container_width=True):
        loaded_player = load_game()
        if loaded_player is not None:
            st.session_state.player = loaded_player
            st.rerun()
        else:
            st.warning("No saved game found.")


# ---------- MAIN GAME ----------
if not player.is_alive():
    st.error("You have been defeated! Load a saved game to continue.")

else:
    st.success(st.session_state.message)

    tab_explore, tab_battle, tab_inventory, tab_stats = st.tabs([
        "🗺️ Explore",
        "⚔️ Battle",
        "🎒 Inventory",
        "📊 Stats"
    ])

    # ---------- EXPLORE ----------
    with tab_explore:
        st.subheader("Explore the World")
        st.write(f"Position: ({player.x}, {player.y})")

        col_left, col_center, col_right = st.columns(3)

        with col_center:
            if st.button("⬆️ North", use_container_width=True):
                game_map.move_player(player, 0, -1)
                st.rerun()

        with col_left:
            if st.button("⬅️ West", use_container_width=True):
                game_map.move_player(player, -1, 0)
                st.rerun()

        with col_right:
            if st.button("➡️ East", use_container_width=True):
                game_map.move_player(player, 1, 0)
                st.rerun()

        with col_center:
            if st.button("⬇️ South", use_container_width=True):
                game_map.move_player(player, 0, 1)
                st.rerun()

        st.markdown("### World Map")

        for y in range(game_map.height):
            row = ""
            for x in range(game_map.width):
                if player.x == x and player.y == y:
                    row += "🧙 "
                elif (x, y) in game_map.locations:
                    row += "📍 "
                else:
                    row += "▫️ "
            st.text(row)

        st.caption("🧙 You | 📍 Location | ▫️ Empty space")

        st.markdown("### Find an Enemy")

        enemy_choice = st.selectbox(
            "Choose an enemy for a test battle",
            ["Goblin", "Wolf", "Orc"]
        )

        if st.button("🔎 Start Battle", use_container_width=True):
            factories = {
                "Goblin": create_goblin,
                "Wolf": create_wolf,
                "Orc": create_orc
            }
            start_battle(factories[enemy_choice]())
            st.session_state.message = (
                f"You encountered a {enemy_choice}!"
            )
            st.rerun()

    # ---------- BATTLE ----------
    with tab_battle:
        st.subheader("Battle Arena")
        enemy = st.session_state.enemy

        if enemy is None:
            st.info("No active battle. Find an enemy in Explore.")
        elif not enemy.is_alive():
            st.info("The enemy has been defeated.")
            st.session_state.enemy = None
        else:
            st.write(f"### 👹 {enemy.name}")
            st.progress(
                max(0.0, min(1.0, enemy.hp / enemy.max_hp)),
                text=f"Enemy HP: {enemy.hp}/{enemy.max_hp}"
            )

            attack_col, potion_col, run_col = st.columns(3)

            with attack_col:
                if st.button("⚔️ Attack", use_container_width=True):
                    damage = random.randint(
                        max(1, player.attack - 4),
                        player.attack + 4
                    )
                    critical = random.randint(1, 100) <= player.crit_chance

                    if critical:
                        damage *= 2
                        add_log("💥 Critical hit!")

                    dealt = enemy.take_damage(damage)
                    add_log(f"You dealt {dealt} damage.")

                    if not enemy.is_alive():
                        finish_battle(enemy)
                    else:
                        enemy.choose_action(player)
                        if not player.is_alive():
                            add_log("You were defeated!")

                    st.rerun()

            with potion_col:
                if st.button("🧪 Use Potion", use_container_width=True):
                    if player.potions > 0 and player.hp < player.max_hp:
                        player.potions -= 1
                        healed = player.heal(30)
                        add_log(f"You recovered {healed} HP.")

                        if enemy.is_alive():
                            enemy.choose_action(player)
                    elif player.potions <= 0:
                        add_log("You have no potions!")
                    else:
                        add_log("Your HP is already full!")

                    st.rerun()

            with run_col:
                if st.button("🏃 Escape", use_container_width=True):
                    add_log("You escaped the battle.")
                    st.session_state.enemy = None
                    st.rerun()

        st.markdown("### Battle Log")
        for entry in reversed(st.session_state.battle_log):
            st.write(f"• {entry}")

    # ---------- INVENTORY ----------
    with tab_inventory:
        st.subheader("Your Inventory")

        st.write(f"🧪 Potions: {player.potions}")

        if player.inventory:
            for item in player.inventory:
                st.write(f"🎒 {item}")
        else:
            st.info("Your inventory is empty.")

        st.markdown("### Equipment")
        st.write(f"⚔️ Weapon: {player.weapon}")
        st.write(f"🛡️ Armor: {player.armor}")

        if st.button("🧪 Drink Potion"):
            if player.potions > 0 and player.hp < player.max_hp:
                player.potions -= 1
                player.heal(30)
                st.success("Potion used!")
            elif player.potions <= 0:
                st.warning("You have no potions.")
            else:
                st.info("Your HP is already full.")
            st.rerun()

    # ---------- STATS ----------
    with tab_stats:
        st.subheader("Character Statistics")

        stats_col1, stats_col2 = st.columns(2)

        with stats_col1:
            st.metric("Level", player.level)
            st.metric("Experience", player.xp)
            st.metric("Critical Chance", f"{player.crit_chance}%")

        with stats_col2:
            st.metric("Attack", player.attack)
            st.metric("Defense", player.defense)
            st.metric("Gold", player.gold)

        st.write(f"**Position:** ({player.x}, {player.y})")
        st.write(f"**Status Effects:** {', '.join(player.status_effects) or 'None'}")
