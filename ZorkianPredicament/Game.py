from Observer import Observer  # Observer of Neighborhood
from Neighborhood import Neighborhood
from Player import Player
import sys
# Author: Sean Aubrey
# Version: 1.0
# for CIS 343


# Game is the starter class for "Zorkian Predicament", a Zork influenced text-based
# game where you must turn the monsters in your neighborhood back into people!
# Game is essentially the controller and view of a MVC design, AKA a 'View-Controller',
# with neighborhood being the head of the model. The view could easily be extracted
# into its own object, but was not deemed necessary given its limited complexity.
#
# Game holds one instance of a single Neighborhood, and a single
# Player. The neighborhood consists of a grid of many homes, each of
# which consists of NPCs. The observer pattern is used to carry update
# information 'downstream' from each NPC back to the Game when the
# NPC is killed. The Player holds one instance of each of its weapons.
class Game(Observer):

    # Instantiate the neighborhood, player, and start the game.
    def __init__(self, max_col, max_row):
        self.__max_col = max_col
        self.__max_row = max_row
        self.__current_col = 0
        self.__current_row = 0
        self.__gameOver = False  # Controls the main game loop.
        self.__options_needed = True  # Whether we will display options text
        self.__neighborhood = Neighborhood(max_col, max_row)
        self.__neighborhood.add_observer(self)  # Add self as observer
        self.__player = Player()
        self.__start()

    # Updates when the neighborhood has been updated that a
    # home has been updated that a monster has been killed, and
    # receives that monster object.
    # @param obj_type
    def update(self, obj_type):
        print("   ", obj_type.get_name(), "transformed back into a person!")
        if self.__check_empty_house() is True:
            print("     Home has been cleared! You're given some more candy. +10 health!")
            self.__player.decrease_health(-10)

    # This is the main game loop, taking user input and prompting game state changes.
    def __start(self):
        print()
        print("You have arrived in a rather Zorkian Predicament.\n"
              "It's Halloween, and something in the candy has turned\n"
              "everyone in your neighborhood into a monster!\n"
              "You find this to be utterly terrifying and terrifically unbelievable,\n"
              "and yet, as far as you know, you are the only one who can do something about it.\n"
              "You must aggressively convince the monsters with candy\n"
              "to return to human form.\n"
              "Good luck. ")

        while self.__gameOver is False:
            if self.__options_needed is True:
                self.__print_options()
            self.__options_needed = True

            decision = self.__prompt_input("Choose a number:", "Your decision must be a number.")

            if decision < 1 or decision > 4:
                print("That's not an option.")
                continue

            # Attack
            if decision == 1:
                if self.__check_empty_house() is True:
                    print(" Home is empty of monsters. ")
                    continue

                # Returns error# 1 if selection out of range,
                # and error# 2 if weapon is 'empty'
                wep_type = self.__choose_weapon()

                if wep_type == 1:
                    print(" That's not an option.")
                    continue

                elif wep_type == 2:
                    print(" That weapon is empty. ")
                    continue

                # Monsters attack back in-turn with player attack
                print(" Attacking!")
                self.__player_attack(wep_type)
                print("\n The monsters retaliate!")
                damage = self.__monster_attack()
                if damage >= 0:
                    print(" You take", damage, "damage!")
                else:
                    damage = abs(damage)
                    print(" You gain", damage, "health!")

            # Moves player
            elif decision == 2:
                if self.__move_player() == 0:
                    print(" You walk to the next house with monsters in it. ")
                else:
                    print(" Through the eyes of a monster still in the house, "
                          "you see a glimmer of the human it once was.\n"
                          " Your compassion compels you to stay and fight, "
                          "even at the cost of your life. ")
                self.__options_needed = False

            # Print neighborhood
            elif decision == 3:
                self.__print_grid()
                self.__options_needed = False

            # Quit
            elif decision == 4:
                print(" You fought bravely.")
                sys.exit(0)

            #  Check if player dead or all monsters defeated
            self.__check_end_condition()

    # Attacks monsters in the current house with the player's attack value
    # depending on the chose weapon.
    # @param wep_type String player's weapon
    def __player_attack(self, wep_type):
        attack_val = self.__player.calc_attack_val(wep_type)
        self.__neighborhood.attack_home(self.__current_row, self.__current_col,
                                        attack_val, wep_type)

    # Collects a sum of damage from all the monsters in the current
    # and applies it to the player's health.
    def __monster_attack(self):
        damage = self.__neighborhood.monster_attack(self.__current_row, self.__current_col)
        self.__player.decrease_health(damage)
        return damage

    # Checks to see if the current home is empty.
    # @return bool True if empty
    def __check_empty_house(self):
        if self.__neighborhood.get_house_num_monsters(
                self.__current_row, self.__current_col) <= 0:
            return True
        return False

    # Prints user's possible decisions.
    def __print_options(self):
        print("\nThere are", self.__neighborhood.get_num_monsters(), "monsters!")
        print("There are", self.__neighborhood.get_num_people(), "people")
        print("Your health:", self.__player.get_health())
        print("1: Attack!")
        print("2: Move")
        print("3: Show the neighborhood")
        print("4: Quit")

    # Takes input to determine the player's weapon to be used in an attack.
    # @return String The name of the chosen weapon.
    def __choose_weapon(self):
        print("\nChoose your weapon: ")
        print("1: Hershey Kiss")
        print("2: Sour Straw - Remaining: ", self.__player.get_num_straws())
        print("3: Chocolate Bar - Remaining: ", self.__player.get_num_bars())
        print("4: Nerd Bomb - Remaining: ", self.__player.get_num_bombs())
        wep_type = self.__prompt_input("Choose your weapon:",
                                       "Your decision must be a number.")

        if wep_type < 1 or wep_type > 4:
            print("That's not an option.")
            return 1

        elif wep_type == 1:
            if self.__player.get_num_kisses() == 0:
                return 2
            return "Hershey Kiss"

        elif wep_type == 2:
            if self.__player.get_num_straws() == 0:
                return 2
            return "Sour Straw"

        elif wep_type == 3:
            if self.__player.get_num_bars() == 0:
                return 2
            return "Chocolate Bar"

        else:
            if self.__player.get_num_bombs() == 0:
                return 2
            return "Nerd Bomb"

    # Loops through and displays neighborhood grid.
    # If a house is empty of monsters, it is displayed as X, else O.
    def __print_grid(self):
        for i in range(self.__max_row):
            for j in range(self.__max_col):

                if i == self.__current_row and j == self.__current_col:
                    print(".", end="")

                if self.__neighborhood.get_house_num_monsters(i, j) <= 0:
                    print("X ", end="")

                else:
                    print("O ", end="")
            print("")

    # Moves the player right to left, top to bottom of the neighborhood
    # grid. If a house has not been cleared of monsters, the player cannot move.
    # @return int 1 if error - house still has monsters
    def __move_player(self):
        if self.__check_empty_house() is True:
            if self.__current_col == (self.__max_col - 1):
                self.__current_row += 1
                self.__current_col = 0
                return 0
            else:
                self.__current_col += 1
                return 0
        else:  # error: House still has monsters
            return 1

    # Check if game has ended, or if all monsters have been transformed
    # or if the player's health has reached zero.
    def __check_end_condition(self):
        if self.__neighborhood.get_num_monsters() == 0:
            self.__player_wins()
        elif self.__player.get_health() <= 0:
            self.__player_defeat()

    # Generic method for getting a user input int given a prompt string.
    # @param prompt_string Let the user know what they should enter.
    # @param error_string Specify that input must be an int.
    # @return int User decision.
    def __prompt_input(self, prompt_string, error_string):
        decision = 0
        try:
            decision = int(input(prompt_string))
        except ValueError:
            print(error_string)
        return decision

    # Only triggered when a player's health has reached zero.
    # Allows the user to start over.
    def __player_defeat(self):
        self.__gameOver = True
        print("\nWith a final strike, you collapse. A person tries to feed you candy,\n"
              "but it's too late. As you exhale for the last time, your eyes remain open,\n"
              "but the world fades to black. It feels like eternity before a light appears\n"
              "in the distance. As it draws nearer you see that it is the ghostly apparition\n"
              "of your father, a veterinarian, turned zombie. Without speaking he communicates\n"
              "that he negotiated the opportunity to bring you back to Earth to try again.\n"
              "Do you accept?")
        print("1: Yes\n2: No")
        decision = int(input())
        while decision > 2 or decision < 1:
            print("1: Yes\n2: No")
            decision = input()
        if decision == 1:
            Game(5, 5)
        else:
            print("You decline, slightly forlorn that you will never see what would have happened\n"
                  "if you had defeated all the monsters, or had looked at the source code.")
            sys.exit(0)

    # Only triggered when the player has transformed all monsters.
    def __player_wins(self):
        self.__gameOver = True
        print("\nYou have transformed all monsters back into humans!\n"
              "Your loved ones hug you, and your crush gives you a smooch!\n"
              "The whole neighborhood throws a party,\n"
              "and everyone offers to help pay you for therapy.\n"
              "You overzealously decline the offers as though what happened was normal,\n"
              "but you can't escape the abyssal hole torn open "
              "in your understanding of reality.\n\n"
              "Something deep within has awoken.\n"
              "You cannot ignore it, and you feel helpless to control it.\n"
              "From an unseen chasm you feel.. a presence.. staring out your own eyes.\n"
              "You feel its hunger - insatiable, bottomless,\n"
              "as though when it was done consuming everything it would turn and consume itself.\n"
              "The more that you fear it, the stronger it becomes, clawing its way into you\n"
              "until, eventually, the fear subsides. For you, as you once knew yourself,\n"
              "have been eclipsed by darkness. Neither a slave, nor a puppet, but the obsidian "
              "heart of the endless void, alone forever.\n\n"
              "You wake up the next morning drenched in sweat. Leaping from the bed,\n"
              "you run to the bathroom and vomit. Your father, a veterinarian, turned zombie,\n"
              "turned human, hears you and comes in. He pats you on the back and says,\n"
              "\"Classic glucose withdrawal. Let it all out, I'll get you some water\".\n"
              "You turn to the camera, breaking 4th wall, and give a hilariously quizzical look.\n"
              "The screen fades to black as you vomit into the toilet.\n")
