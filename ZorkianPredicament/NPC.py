from random import randint
from Observable import Observable  # Observed by a Home
# Author: Sean Aubrey
# Version: 1.0


# Inherited class. Instanced multiple times per home.
# An NPC is-an Observable type, observed by a home.
# NPCs monsters can die and then transform into humans,
# and human NPCs do not take Player damage, and instead
# give the player candy to increase his/her health.
class NPC(Observable):

    # @param name String The type of NPC
    # @param health int NPC's starting health.
    # @param min_attack int Minimum attack value.
    # @param max_attack int Maximum attack value.
    def __init__(self, name, health, min_attack, max_attack):
        super(NPC, self).__init__()  # passes self to Observable
        self._name = name
        self._health = health
        self.__min_attack = min_attack
        self.__max_attack = max_attack

    # Every NPC must be able to take damage from the player.
    # @param attack_val int Player's calculated attack value.
    # @param wep_type String Player's chose weapon type.
    def take_damage(self, attack_val, wep_type):
        raise NotImplementedError

    # Calculates and returns the NPC's attack value, chosen
    # randomly within its set range.
    # @return int Random damage to be applied to the Player.
    def attack(self):
        damage = randint(self.__min_attack, self.__max_attack)
        print("  ", self._name, "does", damage, "damage!")
        return damage

    # Checks if the NPC's health has reached zero, at which point
    # the observing home is updated with the NPC child object type.
    def _check_dead(self):
        if self._health <= 0:
            self.update_observers(self)  # Let the house know that you're dead
            self.remove_all_observers()  # Just the one house, in this case

    def get_name(self):
        return self._name


# Person NPC does not take damage from the Player.
# And, instead of decreasing the player's health,
# a negative attack value is returned to increase it.
class Person(NPC):
    def __init__(self):
        NPC.__init__(self, "Person", 100, 0, 0)

    def take_damage(self, attack_val, wep_type):
        pass

    # Negative means increasing player health
    def attack(self):
        print("   A person gives you some candy. +3 health.")
        return -3


class Zombie(NPC):
    def __init__(self):
        NPC.__init__(self, "Zombie", randint(50, 100), 0, 10)

    def take_damage(self, attack_val, wep_type):
        if wep_type == "Sour Straw":
            attack_val *= 2
            self._health -= attack_val
            print("  ", self._name, "took", attack_val, "damage!")
            print("    The zombie was weak to sour!")
        else:
            self._health -= attack_val
            print("  ", self._name, "took", attack_val, "damage!")
        self._check_dead()


class Vampire(NPC):
    def __init__(self):
        NPC.__init__(self, "Vampire", randint(100, 200), 10, 20)

    def take_damage(self, attack_val, wep_type):
        if wep_type != "Chocolate Bar":
            self._health -= attack_val
            print("  ", self._name, "took", attack_val, "damage!")
            self._check_dead()
        if wep_type == "Chocolate Bar":
            print("   The vampire does not seem to be bothered by chocolate!")


class Ghoul(NPC):
    def __init__(self):
        NPC.__init__(self, "Ghoul", randint(40, 80), 15, 30)

    def take_damage(self, attack_val, wep_type):
        if wep_type == "Nerd Bomb":
            attack_val *= 5
            self._health -= attack_val
            print("  ", self._name, "took", attack_val, "damage!")
            print("    The ghoul was REALLY weak to that Nerd Bomb!")
        else:
            self._health -= attack_val
            print("  ", self._name, "took", attack_val, "damage!")
        self._check_dead()


class Werewolf(NPC):
    def __init__(self):
        NPC.__init__(self, "Werewolf", 200, 0, 40)

    def take_damage(self, attack_val, wep_type):
        if wep_type != "Chocolate Bar" or "Sour Straw":
            self._health -= attack_val
            print("  ", self._name, "took", attack_val, "damage!")
            self._check_dead()
        if wep_type == "Chocolate Bar":
            print("   The Werewolf does not seem to be bothered by chocolate!")
        elif wep_type == "Sour Straw":
            print("   The Werewolf does not seem to mind the taste of sour!")
