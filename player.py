import random

class Player:
    def __init__(self, name):
        self.name = name

        #progression
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

        #combat status
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack= 15
        self.defense= 5
        self.crit_chance= 10

        #Resources
        self.gold = 50
        self.potions = 3

        #equipment
        self.weapon = "Rusty sword"
        self.armor = "Cloth armor"

        #Position
        self.x = 0
        self.y = 0

        #Status
        self.status_effects = []

        #inventory
        self.inventory = []

    def show_stats(self):
        print("="*35)
        print(f"Name: {self.name.upper()}")
        print("="*35)
        print(f"Level:    {self.level}")
        print(f"XP:       {self.xp}/{self.xp_to_next_level}")
        print(f"Attack:   {self.attack}")
        print(f"Defense:  {self.defense}")
        print(f"Crit:     {self.crit_chance}%")
        print(f"Gold:     {self.gold}")
        print(f"Weapon:   {self.weapon}")
        print(f"Armor:    {self.armor}")
        print(f"Position: ({self.x},{self.y})")
        print("=" * 35)

    def move(self, dx , dy):
        self.x += dx
        self.y += dy

    def take_damage(self, damage):
        damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - damage)

        print(f"{self.name} took {damage} damage!")
        return damage
    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        healed= self.hp - old_hp
        print(f"{self.name} healed by {healed} HP!")
        return healed
    def use_potion(self):
        if self.potions <= 0:
            print("you don't have any potions!")
            return False
        if self.hp == self.max_hp:
            print("your hp is already full!")
            return False
        self.potions -= 1
        self.heal(30)

        print(f"Potions remaining: {self.potions}")
        return True
    def attack_enemy(self, enemy):
        damage = random.randit(
            max(1, self.attack - 4),
            self.attack + 4
        )
        critical = random.radint(1, 100) <= self.crit_chance
        if critical:
            damage *= 2
            print("CRITICAL HIT!")
        dealt = enemy.take_damage(damage)
        print(f"you dealt {dealt} damage to {enemy.name}.")
    def gain_xp(self, amount):
        self.xp += amount
        print(f"you gained {amount} XP!")

        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.xp -= self.xp_to_next_level
        self.level += 1

        self.xp_to_next_level = int(
            self.xp_to_next_level * 1.35
        )

        self.max_hp += 20
        self.hp = self.max_hp

        self.attack += 4
        self.defense += 2
        self.crit_chance += 2

        print("=" * 35)
        print(f"Your stats, power, and HP has increased and restored!")

    def add_item(self,item):
        self.inventory.append(item)
        print(f"{item} was added to your inventory!")

    def remove_item(self,item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item} was removed from your inventory.")
            return True
        print(f"you don't have {item}.")
        return False
    def show_inventory(self):
        print("=========== INVENTORY ==============")
        if not self.inventory:
            print("your inventory is empty.")
        else:
            for index, item in enumerate(self.inventory, 1):
                print(f"{index}. {item}")

        print(f"Potions: {self.potions}")
        print("======================================================")

    def equip_weapon(self, weapon, attack_bonus):
        self.weapon = weapon
        self.attack += attack_bonus

        print(f"you equipped {weapon}!")
        print(f"Attack +{attack_bonus}")

    def equip_armor(self, armor, defense_bonus):
        self.armor = armor
        self.defense += defense_bonus

        print(f"you equipped {armor}!")
        print(f"Defense +{defense_bonus}")
    def add_status(self,status):
        if status not in self.status_effects:
            self.status_effects.append(status)
            print(f"Status effect gained: {status}")

    def remove_status(self,status):
        if status in self.status_effect:
            self.status_effect.remove(status)
            print(f"Status effect removed: {status}")

    def is_alive(self):
        return self.hp > 0
    def is_at(self,x,y):
        return self.x == x and self.y ==y

if __name__ == "__main__":
    player = Player("Hero")

    player.show_stats()

    player.add_item("Health Potion")
    player.add_item("Iron Key")
    player.show_inventory()

    player.gain_xp(100)

    player.move(2,3)
    print(f"Current position:  ({player.x},{player.y})")