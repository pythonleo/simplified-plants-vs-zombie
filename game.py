import game_obj as o
import json
import sys
if sys.platform == 'win32':
    from colorama import init
    init()
    init = None
sys = None


class Game:
    def __init__(self):
        self.sunlight = o.sunlight
        self.objects = o.objects
        self.step_num = 0
        with open('level.json') as fr:
            self.steps = json.load(fr)

    def process_command(self, commands):
        for single_command in commands:
            single_command_list = single_command.split()
            if single_command_list[0] == 'plant':
                plant_type = single_command_list[1]
                pos = int(single_command_list[2]) - 1
                if plant_type == 's':
                    o.Sunflower(pos, self.step_num)
                elif plant_type == 'p':
                    o.PeaShooter(pos)
                else:
                    print('Invalid plant type.')
            elif single_command_list[0] == 'remove':
                pos = int(single_command_list[1])
                if isinstance(o.objects[pos - 1], o.Plant):
                    print(o.color(1, 31, "WARNING: The sunlight won't be returned."))
                    res = input("Do you really want to remove position %d?(y/n)" % pos)
                    if res == 'y':
                        o.objects[pos - 1] = 0
            else:
                print('Invalid command.')

    def step(self, commands):
        self.step_num += 1
        self.process_command(commands)
        for obj in self.objects:
            if isinstance(obj, o.GameObject):
                obj.full_step(self.step_num)
        if str(self.step_num) in self.steps.keys():
            if self.steps[str(self.step_num)] == 'zombie':
                o.Zombie()
            elif self.steps[str(self.step_num)] == 'exit zombie':
                o.Zombie(die_to_exit=True)
        self.sunlight = o.sunlight
        self.objects = o.objects

    def start(self):
        while not o.exited:
            print('Sunlight: %d.' % self.sunlight)
            print('Current state:')
            for obj in self.objects:
                print(str(obj), end='  ')
            print()
            first_command = input('next step: ')
            commands = []
            if first_command:
                commands = [first_command]
                while True:
                    command = input('        -: ')
                    if command:
                        commands.append(command)
                    else:
                        break
            self.step(commands)
        if o.plant_win:
            print(o.color(0, 32, "You beat the zombies!"))
        else:
            print(o.color(7, 30, "The zombies are eating your brain!!!"))


print("Welcome to the simplified " + o.color(0, 32, "Plants") + " vs. "\
      + o.color(7, 30, "Zombie") + " game!")
print("Here's the instructions about the game.")
print("Press " + o.color(1, 31, '<ENTER>') + " after you read each instruction.\n" \
      + "Here they are!\n")
input("In this game, you're going to fight against " \
      + "the zombies with your...plants!\n")
input("You have 2 kinds of plants: sunflowers and peashooters.\n")
input("Everything works in a 10*1 grid in this game. And things will " \
      + "change step by step.\n")
input("Meanings of the output:\nYou need 'sunlight' to plant plants." \
      + "A sunflower needs 50 sunlight and 100 for a peashooter.\n" \
      + "'Current state' outputs the current game grid, " \
      + "where 's' means a sunflower, 'p' stands for a peashooter, " \
      + "'z' symbolizes a zombie and '0' is an empty grid. "\
      + "And the 'next step' prompt wants you to enter a command "\
      + "for the next step.\n")
input("For example:\nSunlight: 50.\nCurrent state:\n" + '0  ' * 10 \
      + "\nThat means you have 50 sunlight and an empty grid.\n")
input("Plant your plants using 'plant type pos' commands "\
      + "in the 'next step' prompt, " \
      + "in which 'type' means the type of the plant " \
      + "(s for sunflower and p for peashooter), "\
      + "and 'pos' means the position you want to plant it " \
      + "(starting with 1 from left to right).\n")
input("For example:\nnext step: plant s 1\n" \
      + "That means to plant a sunflower on the very left grid.\n")
input("So how do your plants fight with the zombies?\n" \
      + "As you can see, planting plants needs sunlight. " \
      + "But only 50 sunlight is given. So you need sunflowers " \
      + "to produce sunlight for you. A sunflower produces 50 " \
      + "sunlight every 2 steps.\nPeashooters are real fighters. "\
      + "A peashooter attacks the nearest zombie in front of it "\
      + "every step. The zombie will die after a few steps. \n")
input("Ahh! A plant is planted in a wrong position. In this case, " \
      + "you can remove it by using 'remove pos' commands in the " \
      + "'next step' prompt, where 'pos' is the position of the plant " \
      + "you want to remove. But the sunlight won't be returned to you. " \
      + "So, think it over before you plant something.\n")
input("No more instructions! Ready for a challenge? (just "\
      + o.color(1, 31, '<ENTER>') + ")\n")
Game().start()
