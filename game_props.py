import game_obj as o
import json
import sys
import os
if sys.platform == 'win32':
    from colorama import init
    init()
    init = None
sys = None


class Game:
    def __init__(self):
        o.sunlight = 50
        o.exited = False
        o.plant_win = False
        o.objects = [([0] * 10) for i in range(5)]
        self.sunlight = o.sunlight
        self.objects = o.objects
        self.step_num = 0
        self.kickers = []
        with open('level.txt') as lv:
            try:
                with open('levels/%s.json' % lv.read()) as fw:
                    self.steps = json.load(fw)
            except FileNotFoundError:
                with open('levels/0.json') as fw:
                    self.steps = json.load(fw)
                with open('level.txt', 'w') as lv_w:
                    lv_w.write('0')

    def process_command(self, commands):
        for single_command in commands:
            single_command_list = single_command.split()
            if single_command_list[0] == 'plant':
                try:
                    plant_type = single_command_list[1]
                    x = int(single_command_list[2]) - 1
                    y = 5 - int(single_command_list[3])
                except (IndexError, ValueError):
                    print(o.color(31, 'Invalid command.'))
                else:
                    if plant_type == 's':
                        o.Sunflower(x, y, self.step_num)
                    elif plant_type == 'p':
                        o.PeaShooter(x, y)
                    else:
                        print(o.color(31, 'Invalid plant type.'))
            elif single_command_list[0] == 'remove':
                try:
                    x = int(single_command_list[1])
                    y = int(single_command_list[2])
                except (IndexError, ValueError):
                    print(o.color(31, 'Invalid command.'))
                else:
                    if isinstance(o.objects[y - 1][x - 1], o.Plant):
                        print(o.color(31, ("WARNING: The sunlight won't be returned.\n"
                                      + "Do you really want to remove position (%d, %d)?(y/n)")
                                      % (x, y)), end='')
                        res = input()
                        if res == 'y':
                            o.objects[y - 1][x - 1] = 0
            else:
                print(o.color(31, 'Invalid command.'))

    def step(self, commands):
        from random import randint as r
        self.step_num += 1
        self.process_command(commands)
        for l in self.objects:
            for obj in l:
                if isinstance(obj, o.GameObject):
                    obj.full_step(self.step_num)
            for obj in l:
                if isinstance(obj, o.GameObject):
                    obj.full_check()
        if self.kickers:
            zombies = [0] * 5
            for kicker in self.kickers:
                zombies[kicker - 5] = o.KickerZombie(kicker - 5)
            for i, zombie in enumerate(zombies):
                if zombie == 0:
                    zombies[i] = o.Zombie(i)
            self.kickers = []
        if str(self.step_num) in self.steps.keys():
            from config import config
            if self.steps[str(self.step_num)] == "wave" \
                    and not self.kickers:
                print(o.color(31, "A huge wave of zombies is approaching!"))
                o.sleep(0.3)
                kickers = []
                for i in range(10):
                    new = r(0, 9)
                    if new not in kickers:
                        kickers.append(new)
                kickers.sort()
                kickers_now = []
                for kicker in kickers:
                    if kicker < 5:
                        kickers_now.append(kicker)
                    else:
                        self.kickers.append(kicker)
                zombies = [0] * 5
                for kicker in kickers_now:
                    zombies[kicker] = o.KickerZombie(kicker)
                for i, zombie in enumerate(zombies):
                    if zombie == 0:
                        zombies[i] = o.Zombie(i)
            elif not self.kickers:
                config_command = self.steps[str(self.step_num)].split()
                die_to_exit = len(config_command) == 2
                if die_to_exit:
                    del config_command[0]
                config["zombie_names"][config_command[0]](r(0, 4), die_to_exit=die_to_exit)

        self.sunlight = o.sunlight
        self.objects = o.objects

    def start(self):
        while not o.exited:
            print('Sunlight: %d.' % self.sunlight)
            print('Current state:')
            for l in self.objects:
                for obj in l:
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
            print(o.color(31, "You beat the zombies!"))
            o.sleep(0.3)
            with open('level.txt') as fr:
                current_level = int(fr.read())
            with open('level.txt', 'w') as lv_w:
                lv_w.write(str(current_level + 1))
            os.popen("git commit -am \"commit level change\"")
        else:
            print(o.color(31, "The zombies are eating your brain!!!"))
            o.sleep(0.3)

        def str_or_num(num, string):
            return string if not num else str(num)

        print("You planted %s plants in all." % str_or_num(o.all_plants, 'no'))
        o.sleep(0.3)
        print("%s of them are killed by zombies." % str_or_num(o.dead_plants, 'None'))
        o.sleep(0.3)
        print("There are %s zombies in all." % str_or_num(o.all_zombies, 'no'))
        o.sleep(0.3)
        print("You killed %s of them."
              % (str_or_num(o.dead_zombies, 'none')
                 if o.all_zombies != o.dead_zombies else 'all'))
        o.sleep(0.3)
