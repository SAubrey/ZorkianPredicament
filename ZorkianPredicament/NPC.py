from random import randint
from Observable import Observable  # Observed by a Home


# A monster or person is an NPC, which is an Observable object
class NPC(Observable):
    def __init__(self, name, health, min_attack, max_attack):
        super(NPC, self).__init__()  # passes self to Observable
        self._name = name
        self._health = health
        self.__min_attack = min_attack
        self.__max_attack = max_attack

    def take_damage(self, attack_val, wep_type):
        raise NotImplementedError

    def attack(self):
        damage = randint(self.__min_attack, self.__max_attack)
        print("  ", self._name, "does", damage, "damage!")
        return damage

    def _check_dead(self):
        if self._health <= 0:
            self.update_observable(self)  # Let the house know that you're dead
            self.remove_all_observers()  # Just the one house, in this case

    def get_name(self):
        return self._name

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
