from random import randint
from Observer import Observer  # Observer of Monsters
from Observable import Observable  # Observed by Neighborhood
from NPC import Person, Zombie, Vampire, Ghoul, Werewolf


class Home(Observer, Observable):
    def __init__(self):
        super(Home, self).__init__()  # passes self to Observable
        self.__num_monsters = 0
        self.__num_people = 0
        self.__NPC_list = []
        self.__population_size = randint(0, 10)
        self.__spawn_NPCs(self.__population_size)

    # Observer update - called when monster killed
    def update_observer(self, obj_type):
        self.__num_monsters -= 1
        self.__NPC_list.remove(obj_type)
        super().update_observable(obj_type)  # Updating the neighborhood

        self.__num_people += 1
        p = Person()
        self.__NPC_list.append(p)
        p.add_observer(self)

    def monster_attack(self):
        damage = 0
        for i in self.__NPC_list:
            damage += i.attack()
        return damage

    def take_attack(self, attack_val, wep_type):
        for i in self.__NPC_list:
            i.take_damage(attack_val, wep_type)

    #  Create monsters, add this home as an observer
    #  to every monster.
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

