from random import randint
from Weapon import HersheyKiss, SourStraw, ChocolateBar, NerdBomb


class Player:
    def __init__(self):
        self.__health = randint(100, 125)
        self.__min_attack_val = 10
        self.__max_attack_val = 20
        self.__inventory_size = 10
        __num_kisses = 1
        __num_straws = 0
        __num_bars = 0
        __num_bombs = 0
        self.__inventory = \
            {'Hershey Kiss': {'obj': HersheyKiss(), 'num': __num_kisses},
             'Sour Straw': {'obj': SourStraw(), 'num': __num_straws},
             'Chocolate Bar': {'obj': ChocolateBar(), 'num': __num_bars},
             'Nerd Bomb': {'obj': NerdBomb(), 'num': __num_bombs}}

        self.__fill_inventory()

    def decrease_health(self, num):
        self.__health -= num

    def calc_attack_val(self, wep_type):
        attack_val = randint(self.__min_attack_val, self.__max_attack_val)
        attack_val *= float(self.__inventory[wep_type]['obj'].use_weapon())
        self.__expire_weapon(wep_type)
        return attack_val

    def __fill_inventory(self):
        for i in range(0, self.__inventory_size):
            wep_type = randint(1, 3)

            if wep_type == 1:
                self.__inventory['Sour Straw']['num'] += 1
            elif wep_type == 2:
                self.__inventory['Chocolate Bar']['num'] += 1
            else:
                self.__inventory['Nerd Bomb']['num'] += 1

    def __expire_weapon(self, wep_type):
        weapon = self.__inventory[wep_type]
        if weapon['obj'].get_remaining_uses() == 0:
            if weapon['num'] != 0:
                self.__inventory[wep_type]['num'] -= 1
                self.__inventory[wep_type]['obj'].reset_num_uses()

    def get_health(self):
        return self.__health

    def get_num_kisses(self):
        return self.__inventory['Hershey Kiss']['num']

    def get_num_straws(self):
        return self.__inventory['Sour Straw']['num']

    def get_num_bars(self):
        return self.__inventory['Chocolate Bar']['num']

    def get_num_bombs(self):
        return self.__inventory['Nerd Bomb']['num']
