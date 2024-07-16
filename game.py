import random
import json

# Character Class
class Character:
    def __init__(self, name, health, attack, defense, magic):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.experience = 0
        self.level = 1
        self.inventory = []
        self.alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.health = 0

    def attack_enemy(self, enemy):
        damage = max(0, self.attack - enemy.defense)
        enemy.take_damage(damage)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")

    def cast_spell(self, enemy, spell):
        if spell in self.magic:
            damage = self.magic[spell]
            enemy.take_damage(damage)
            print(f"{self.name} casts {spell} on {enemy.name} for {damage} damage!")
        else:
            print(f"{self.name} doesn't know the spell {spell}.")

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 10
        self.health = self.max_health
        self.attack += 2
        self.defense += 2
        print(f"{self.name} leveled up to level {self.level}!")

    def use_item(self, item):
        if item in self.inventory:
            if item == "Health Potion":
                self.health = min(self.max_health, self.health + 20)
                print(f"{self.name} uses a Health Potion and restores 20 health.")
            elif item == "Attack Potion":
                self.attack += 5
                print(f"{self.name} uses an Attack Potion and gains 5 attack.")
            self.inventory.remove(item)
        else:
            print(f"{self.name} doesn't have a {item}.")

    def __str__(self):
        return (f"{self.name} (Level: {self.level}, HP: {self.health}/{self.max_health}, "
                f"ATK: {self.attack}, DEF: {self.defense}, EXP: {self.experience}/100)")

# Enemy Class
class Enemy:
    def __init__(self, name, health, attack, defense, exp_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.health = 0

    def attack_character(self, character):
        damage = max(0, self.attack - character.defense)
        character.take_damage(damage)
        print(f"{self.name} attacks {character.name} for {damage} damage!")

    def __str__(self):
        return f"{self.name} (HP: {self.health}/{self.max_health}, ATK: {self.attack}, DEF: {self.defense})"

# NPC Class
class NPC:
    def __init__(self, name, dialog):
        self.name = name
        self.dialog = dialog

    def talk(self):
        print(f"{self.name}: {self.dialog}")

# Game Class
class Game:
    def __init__(self, player):
        self.player = player
        self.enemies = [
            Enemy("Goblin", 30, 5, 2, 20),
            Enemy("Orc", 50, 7, 3, 30),
            Enemy("Dragon", 100, 10, 5, 50)
        ]
        self.current_enemy = None
        self.locations = {
            "Forest": ["Goblin", "Orc"],
            "Cave": ["Orc", "Dragon"],
            "Castle": ["Dragon"]
        }
        self.current_location = None
        self.npcs = [
            NPC("Old Man", "Beware of the dragon in the castle!"),
            NPC("Merchant", "I have potions for sale."),
        ]

    def start_battle(self, enemy):
        self.current_enemy = enemy
        print(f"A wild {enemy.name} appears!")

        while self.player.alive and enemy.alive:
            self.player_turn()
            if enemy.alive:
                self.enemy_turn()

        if self.player.alive:
            print(f"You defeated the {enemy.name}!")
            self.player.gain_experience(enemy.exp_reward)
        else:
            print(f"You were defeated by the {enemy.name}...")

    def player_turn(self):
        print(f"Player's turn:")
        action = input("Choose an action: (attack/cast/use/talk/quit): ").lower()
        if action == "attack":
            self.player.attack_enemy(self.current_enemy)
        elif action == "cast":
            spell = input("Enter the spell to cast: ")
            self.player.cast_spell(self.current_enemy, spell)
        elif action == "use":
            item = input("Enter the item to use: ")
            self.player.use_item(item)
        elif action == "talk":
            for npc in self.npcs:
                npc.talk()
        elif action == "quit":
            self.save_game()
            print("Game saved. Thanks for playing!")
            exit()
        else:
            print("Invalid action.")

        print(self.current_enemy)

    def enemy_turn(self):
        print(f"Enemy's turn:")
        self.current_enemy.attack_character(self.player)
        print(self.player)

    def explore(self):
        print("Exploring the world...")
        if random.choice([True, False]):
            location = random.choice(list(self.locations.keys()))
            self.current_location = location
            print(f"You arrive at the {location}.")
            if random.choice([True, False]):
                enemy_name = random.choice(self.locations[location])
                enemy = next(e for e in self.enemies if e.name == enemy_name)
                self.start_battle(enemy)
            else:
                item = random.choice(["Health Potion", "Attack Potion"])
                self.player.inventory.append(item)
                print(f"You found a {item}!")
        else:
            print("You find nothing interesting.")

    def save_game(self):
        save_data = {
            "name": self.player.name,
            "health": self.player.health,
            "max_health": self.player.max_health,
            "attack": self.player.attack,
            "defense": self.player.defense,
            "magic": self.player.magic,
            "experience": self.player.experience,
            "level": self.player.level,
            "inventory": self.player.inventory
        }
        with open("save_game.json", "w") as file:
            json.dump(save_data, file)
        print("Game saved successfully.")

    def load_game(self):
        try:
            with open("save_game.json", "r") as file:
                save_data = json.load(file)
                self.player = Character(
                    save_data["name"],
                    save_data["max_health"],
                    save_data["attack"],
                    save_data["defense"],
                    save_data["magic"]
                )
                self.player.health = save_data["health"]
                self.player.experience = save_data["experience"]
                self.player.level = save_data["level"]
                self.player.inventory = save_data["inventory"]
            print("Game loaded successfully.")
        except FileNotFoundError:
            print("No saved game found.")

# Main Game Loop
def main():
    print("Welcome to the Text-Based RPG Game!")
    print("1. New Game")
    print("2. Load Game")
    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter your character's name: ")
        player = Character(name, 100, 10, 5, {"Fireball": 15, "Heal": -10})
        game = Game(player)
    elif choice == "2":
        game = Game(None)
        game.load_game()
        player = game.player
    else:
        print("Invalid choice.")
        return

    print(f"Welcome, {player.name}!")
    print(player)

    while player.alive:
        action = input("What would you like to do? (explore/quit): ").lower()
        if action == "explore":
            game.explore()
        elif action == "quit":
            game.save_game()
            print("Game saved. Thanks for playing!")
            break
        else:
            print("Invalid action. Please choose 'explore' or 'quit'.")

    if not player.alive:
        print("Game Over. Better luck next time!")

if __name__ == "__main__":
    main()
