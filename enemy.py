import random


class Enemy:
    def __init__(
        self,
        name,
        hp,
        attack,
        defense,
        xp_reward,
        gold_reward,
        ability=None
    ):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense

        self.xp_reward = xp_reward
        self.gold_reward = gold_reward

        self.ability = ability
        self.defending = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        if self.defending:
            damage = damage // 2
            self.defending = False
            print(f"{self.name} blocked part of the attack!")

        actual_damage = max(1, damage - self.defense)

        self.hp = max(0, self.hp - actual_damage)

        return actual_damage

    def basic_attack(self, player):
        damage = random.randint(
            max(1, self.attack - 4),
            self.attack + 4
        )

        actual_damage = player.take_damage(damage)

        print(
            f"{self.name} attacked you "
            f"for {actual_damage} damage!"
        )

    def defend(self):
        self.defending = True
        print(f"{self.name} is defending!")

    def use_ability(self, player):
        if self.ability == "poison":
            damage = 8
            player.take_damage(damage)

            player.add_status("Poisoned")

            print(
                f"{self.name} used Poison!"
            )

        elif self.ability == "heavy_attack":
            damage = random.randint(
                self.attack + 5,
                self.attack + 12
            )

            player.take_damage(damage)

            print(
                f"{self.name} used Heavy Attack!"
            )

        else:
            self.basic_attack(player)

    def choose_action(self, player):
        roll = random.randint(1, 100)

        if self.ability and roll <= 20:
            self.use_ability(player)

        elif roll <= 35:
            self.defend()

        else:
            self.basic_attack(player)


def create_goblin():
    return Enemy(
        "Goblin",
        60,
        12,
        3,
        35,
        20,
        "poison"
    )


def create_wolf():
    return Enemy(
        "Wolf",
        45,
        16,
        2,
        30,
        15,
        None
    )


def create_orc():
    return Enemy(
        "Orc",
        100,
        20,
        7,
        70,
        40,
        "heavy_attack"
    )