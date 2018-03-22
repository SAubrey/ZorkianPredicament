from Home import Home
from Observer import Observer  # Observer of Houses
from Observable import Observable  # Observed by Game
# Author: Sean Aubrey
# Version: 1.0


# Neighborhood is instanced once per game. It is-a type of Observer to each home,
# and is-a type of Observable to Game. A neighborhood consists of a
# grid of homes, each of which updates the neighborhood.
# Neighborhood is responsible for accessing each home.
class Neighborhood(Observer, Observable):

    # Creates a grid of homes of a set row and column size. The neighborhood
    # adds itself as an observer to each home.
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

    # Updates Game when a Home updates that a monster has been killed
    # and returns the type of monster that has been killed.
    # @param obj_type NPC obj type that has been killed.
    def update(self, obj_type):
        self.__total_num_monsters -= 1
        self.__total_num_people += 1
        super().update_observers(obj_type)  # Update the Game

    # Lets a particular home know to apply an amount of damage to its monsters.
    # @param current_row The row the player is at.
    # @param current_col The column the player is at.
    # @param attack_val int The player's calculated attack value.
    # @param wep_type String The player's chosen weapon.
    def attack_home(self, current_row, current_col, attack_val, wep_type):
        self.__home_grid[current_row][current_col].take_attack(attack_val, wep_type)

    # Retrieves a sum of damage of the monsters at a particular home.
    # @param current_row The row the player is at.
    # @param current_col The column the player is at.
    # @return Sum of monster's damage.
    def monster_attack(self, current_row, current_col):
        return self.__home_grid[current_row][current_col].monster_attack()

    # Loops through each home in the grid and retrieves the number of
    # remaining monsters.
    # @return The sum of monsters remaining in the neighborhood.
    def __count_monsters(self):
        total_num_monsters = 0
        for i in range(self.max_row):
            for j in range(self.max_col):
                total_num_monsters += self.__home_grid[i][j].get_num_monsters()
        return total_num_monsters

    # Loops through each home in the grid and retrieves the number of
    # people.
    # @return The sum of people in the neighborhood.
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
