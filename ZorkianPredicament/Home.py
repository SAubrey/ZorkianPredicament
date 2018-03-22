from random import randint
from Observer import Observer  # Observer of Monsters
from Observable import Observable  # Observed by Neighborhood
from NPC import Person, Zombie, Vampire, Ghoul, Werewolf
# Author: Sean Aubrey
# Version: 1.0


# Instanced once per grid element in the neighborhood.
# A home is-a Observer of each NPC within it, and
# is-a Observable, observed by the Neighborhood.
class Home(Observer, Observable):

    # Sets a random population within the home and
    # spawns that population.
    def __init__(self):
        super(Home, self).__init__()  # passes self to Observable
        self.__num_monsters = 0
        self.__num_people = 0
        self.__NPC_list = []
        self.__population_size = randint(0, 10)
        self.__spawn_NPCs(self.__population_size)

    # Updated when a monster is killed, so that the home
    # can update the neighborhood that a type of monster has been killed.
    # When a monster is killed it is transformed into a person, so we
    # create a person to take its place.
    # @param obj_type NPC obj The killed monster.
    def update(self, obj_type):
        self.__num_monsters -= 1
        self.__NPC_list.remove(obj_type)
        super().update_observers(obj_type)  # Updating the neighborhood

        self.__num_people += 1
        p = Person()
        self.__NPC_list.append(p)
        p.add_observer(self)

    # Sums the amount of damage to be applied to the player
    # from each monster in the house.
    # @return int Sum of monster damage.
    def monster_attack(self):
        damage = 0
        for i in self.__NPC_list:
            damage += i.attack()
        return damage

    # Applies the player's calculated damage to each NPC
    # in the home.
    # @param attack_val int Player's calculated damage.
    # @param wep_type String Player's chose weapon type.
    def take_attack(self, attack_val, wep_type):
        for i in self.__NPC_list:
            i.take_damage(attack_val, wep_type)

    # Called once per game instance to randomly spawn NPCs.
    # The Home is passed to each NPC as its observer.
    # @param population_size int Home's max population size.
    def __spawn_NPCs(self, population_size):
        for _ in range(0, population_size):
            NPC_type = randint(1, 4)

            if NPC_type == 1:  # Person
                p = Person()
                self.__NPC_list.append(p)
                p.add_observer(self)
                self.__num_people += 1

            elif NPC_type == 2:  # Zombie
                z = Zombie()
                self.__NPC_list.append(z)
                z.add_observer(self)
                self.__num_monsters += 1

            elif NPC_type == 3:  # Vampire
                v = Vampire()
                self.__NPC_list.append(v)
                v.add_observer(self)
                self.__num_monsters += 1

            elif NPC_type == 4:  # Ghoul
                g = Ghoul()
                self.__NPC_list.append(g)
                g.add_observer(self)
                self.__num_monsters += 1

            else:                # Werewolf
                w = Werewolf()
                self.__NPC_list.append(w)
                w.add_observer(self)
                self.__num_monsters += 1

    def get_num_monsters(self):
        return self.__num_monsters

    def get_num_people(self):
        return self.__num_people

