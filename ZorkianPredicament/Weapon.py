from random import uniform
# Author: Sean Aubrey
# Version: 1.0


# Inherited class. One instance of each type of weapon
# exists in the player's inventory. Each weapon keeps track of
# its number of uses.
class Weapon:
    def __init__(self, min_attack_mod, max_attack_mod, max_num_uses):
        self.__min_attack_mod = min_attack_mod
        self.__max_attack_mod = max_attack_mod
        self.__max_num_uses = max_num_uses
        self.__num_uses = max_num_uses

    # Decreases the weapon's number of uses by one.
    def use_weapon(self):
        self.__num_uses -= 1
        return uniform(self.__min_attack_mod, self.__max_attack_mod)

    # Set's the weapon's number of uses to zero.
    def reset_num_uses(self):
        self.__num_uses = self.__max_num_uses

    def get_remaining_uses(self):
        return self.__num_uses


# Hershey Kisses can be used infinitely, though a
# large finite number will suffice per game instance.
class HersheyKiss(Weapon):
    def __init__(self):
        Weapon.__init__(self, 1, 1, 10000)


class SourStraw(Weapon):
    def __init__(self):
        Weapon.__init__(self, 1, 1.75, 2)


class ChocolateBar(Weapon):
    def __init__(self):
        Weapon.__init__(self, 2, 2.4, 4)


class NerdBomb(Weapon):
    def __init__(self):
        Weapon.__init__(self, 3.5, 5, 1)
