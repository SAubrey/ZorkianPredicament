from Home import Home
from Observer import Observer  # Observer of Houses
from Observable import Observable  # Observed by Game


# Neighborhood is updated by its homes
class Neighborhood(Observer, Observable):
    def __init__(self, max_col, max_row):
        super(Neighborhood, self).__init__()
        self.max_col = max_col
        self.max_row = max_row

        self.__home_grid = [[Home() for x in range(max_col)] for y in range(max_row)]
        for i in range(self.max_row):
            for j in range(self.max_col):
                self.__home_grid[i][j].add_observer(self)
        self.__total_num_monsters = self.__count_monsters()
        self.__total_num_people = self.__count_people()

    #  Updates Game when a Home updates that a monster has been killed
    def update_observer(self, obj_type):
        self.__total_num_monsters -= 1
        self.__total_num_people += 1
        super().update_observable(obj_type)  # Update the Game

    def attack_home(self, current_row, current_col, attack_val, wep_type):
        self.__home_grid[current_row][current_col].take_attack(attack_val, wep_type)

    def monster_attack(self, current_row, current_col):
        return self.__home_grid[current_row][current_col].monster_attack()

    def __count_monsters(self):
        total_num_monsters = 0
        for i in range(self.max_row):
            for j in range(self.max_col):
                total_num_monsters += self.__home_grid[i][j].get_num_monsters()
        return total_num_monsters

    def __count_people(self):
        total_num_people = 0
        for i in range(self.max_row):
            for j in range(self.max_col):
                total_num_people += self.__home_grid[i][j].get_num_people()
        return total_num_people

    def get_num_monsters(self):
        return self.__total_num_monsters

    def get_house_num_monsters(self, current_row, current_col):
        return self.__home_grid[current_row][current_col].get_num_monsters()

    def get_num_people(self):
        return self.__total_num_people
