import random
from random import randrange

## CONSTANTS ##

##Art by Hayley Jane Wakenshaw - https://www.asciiart.eu/animals/dogs
DOG_LEFT = """
   __
o-''|\_____/)
 \_/|_)     )
    \  __  /
    (_/ (_/ 
"""

DOG_RIGHT = """
        __
(\_____/|''-o
(     (_|\_/
 \  __   / 
  \_) \_) 
"""

##Art by Joan Stark - https://www.asciiart.eu/animals/cats
CAT_LEFT = """
 /\    /    
(' )  (
 (  \  )
 |(__)/
"""

CAT_RIGHT = """
\    /\\
 )  ( ')
(  /  )
 \(__)|
"""


class Pet:
    '''A Tamagotchi pet!
    Attributes
    ----------
    name : string
        The pet's name
    '''
    max_boredom = 6
    max_hunger = 10
    leaves_hungry = 16
    leaves_bored = 12


    def __init__(self, name, sound):
        self.name = name
        self.hunger = randrange(self.max_hunger)
        self.boredom = randrange(self.max_boredom)
        self.sound = sound
        self.type = resp_pet_type.lower()
        self.age = 0
        if self.type == 'cat':
            self.ascii_art_left = CAT_LEFT
            self.ascii_art_right = CAT_RIGHT
        else:
            self.ascii_art_left = DOG_LEFT
            self.ascii_art_right = DOG_RIGHT

    def mood(self):
        '''Get the mood of a pet. A pet can be happy, hungry or bored,
        depending on wether it was fed or has played enough.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The mood of the pet
        '''
        if self.hunger <= self.max_hunger and self.boredom <= self.max_boredom:
            return "happy"
        elif self.hunger > self.max_hunger:
            return "hungry"
        else:
            return "bored"

    def status(self):
        '''Get the status of a pet to know it's name, how it feels and what it wants.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The name, mood and wants of the pet.
        '''
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Please feed me.'
        if self.mood() == 'bored':
            state += 'You can play with me.'
        return state

    def do_command(self, resp):
        '''Calls the appropriate methods of a pet based on command "resp" given by player.

        Parameters
        ----------
        resp : string
            The command to be issued to the pet.

        Returns
        -------
        none
        '''
        resp = resp.lower()
        if self.type == 'poodle':
            if resp == "speak":
                print(self.speak())
            elif resp == "play":
                self.play()
            elif resp == "feed":
                self.feed()
            elif resp == "wait":
                print("Poodles cannot wait, please provide avalid command.")
            elif resp == 'dance':
                print("Dancing in circles like poodles do!")
            else:
                print("Please provide a valid command.")
        elif self.type == 'dog':
            if resp == "speak":
                print(self.speak())
            elif resp == "play":
                self.play()
            elif resp == "feed":
                self.feed()
            elif resp == "wait":
                print("Dogs cannot wait, please provide avalid command.")
            else:
                print("Please provide a valid command.")
        else:
            if resp == "speak":
                print(self.speak())
            elif resp == "play":
                self.play()
            elif resp == "feed":
                self.feed()
            elif resp == "wait":
                print("Nothing to do...")
            else:
                print("Please provide a valid command.")

    def has_left(self):
        '''Returns True if a pet has left the game due to hunger or boredom, otherwise False.

        Parameters
        ----------
        none

        Returns
        -------
        bool
            If a pet has left
        '''
        return self.hunger > self.leaves_hungry or self.boredom > self.leaves_bored or int(self.age) > 18

    def clock_tick(self):
        '''Adds a time path which changes the boredom level and hunger level of the pet.

        Parameters
        ----------
        none

        Returns
        -------
        none
        '''
        self.boredom += 2
        self.hunger += 2
        if self.type == 'dog':
            self.age += 2
        elif self.type == 'cat':
            self.age += 3
        elif self.age == 'poodle':
            self.age += 2.5

    def speak(self):
        '''
        This runs when the “speak” command is issued. Print the pet’s unique sound.

        Parameters
        ----------
        none

        Returns
        -------
        string
        '''
        return "I say: " + str(self.sound)

    def feed(self):
        '''
        This runs when the“feed” command is issued. The pet’s hunger isdecreased by 5.

        Parameters
        ----------
        none

        Returns
        -------
        none
        '''
        self.hunger -= 5
        if self.hunger < 0:
            self.hunger = 0

    def play(self):
        '''
        The user tries to guess which way the pet will look up to 3 times.
        If they guess correctly, the play is done and the pet’s boredom is decreased by 5
        If they guess incorrectly all 3 times, the game ends

        Parameters
        ----------
        none

        Returns
        -------
        none
        '''
        direction = ['left', 'right']
        if self.type == 'cat':
            count = 5
        else:
            count = 3
        while count > 0:
            guess = input("Which way your pet will look? Guess left/right: ")
            guess = guess.lower()
            direction_random = random.choice(direction)
            try:
                if guess == direction_random:
                    self.boredom -= 5
                    print("Correct!")
                    break
                elif guess != direction_random:
                    if guess == 'right' and direction_random == 'left':
                        print("I look to the left. Try again. " + str(count - 1) + " chances left.")
                        print(self.ascii_art_left)
                        count -= 1
                    elif guess == 'left' and direction_random == 'right':
                        print("I look to the right. Try again. " + str(count - 1) + " chances left.")
                        print(self.ascii_art_right)
                        count -= 1
                    else:
                        print("Only 'left' and 'right' are valid guesses. Try again.")
            except:
                continue


#######################################################################
# ---------- Part 2: Inheritance - subclasses
#######################################################################

class Dog(Pet):
    def __init__(self, name, sound):
        super().__init__(name, sound)
        self.type = 'dog'

    def speak(self):
        '''
        This runs when the “speak” command is issued. Print the pet’s unique sound.
        Parameters
        ----------
        none

        Returns
        -------
        string
        '''
        return "I say: " + str(self.sound) + " arrrf!"


class Cat(Pet):
    def __init__(self, name, sound, meow_count):
        super().__init__(name, sound)
        self.meow_count = meow_count
        self.type = 'cat'

    def speak(self):
        '''
        This runs when the “speak” command is issued. Print the pet’s unique sound.
        Parameters
        ----------
        none

        Returns
        -------
        string
        '''
        return "I say: " + str(self.sound) * int(self.meow_count)


class Poodle(Dog):
    def __init__(self, name, sound):
        super().__init__(name, sound)
        self.type = 'poodle'

    def dance(self):
        return "Dancing in circles like poodles do!"

    def speak(self):
        return str(self.dance()) + "\n I say: " + str(self.sound) + " arrrf!"


def get_name():
    '''Asks the player which name a pet should have.

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    return input("How do you want to name your pet?\n")


def get_sound():
    '''Asks the player what sound a pet should make

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    return input("What does your pet say (e.g. woof, meow, yo)?\n ")


def get_meow_count():
    '''Asks the player how often a cat should make a sound.

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    while True:
        resp = input("How often does your Cat make a sound?\n")
        if resp.isnumeric():
            return int(resp)

while True:
    p = None
    while p == None:
        add_p = input("Would you like to adopt a pet? Y/N \n")
        pets = {}
        while add_p == 'Y':
            resp_pet_type = input("What kind of pet would you like to adopt?\n").lower()
            if resp_pet_type in ['dog','cat','poodle']:
                name = get_name()
                pets[name]=resp_pet_type
                add_p = input("Would you like to adopt a pet? Y/N \n")
                print("Now, you have", pets)
            else:
                print("We only have Cat, Dog and Poodle.")
                continue

        call = input("Please type one of your pets' name to call him out: \n")
        if pets[call] == 'dog':
            sound = get_sound()
            p = Dog(name, sound)
        elif pets[call] == 'cat':
            sound = get_sound()
            meow_count = get_meow_count()
            p = Cat(name, sound, meow_count)
        elif pets[call] == 'poodle':
            sound = get_sound()
            p = Poodle(name, sound)

        while not p.has_left():
            print()
            print(p.status())

            command = input("What should I do?\n")
            p.do_command(command)
            p.clock_tick()

        print("Your pet",call,"has left.")

    again = input("Would you like to play again? Y/N \n")
    if again == "N":
        break

