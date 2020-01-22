from time import sleep
from random import randint as r
from grade_ability import grade_ability as ga
import json

# base settings
objects = [[0] * 10 for i in range(5)]    # game board
sunlight = 50                             # sunlight, initial value 50
# exit flags
exited = False                            # is game exiting
plant_win = False                         # is plants winning
# stats
all_plants = 0
dead_plants = 0
all_zombies = 0
dead_zombies = 0
# caves
caves = {}


def color(font, text):
    return "\033[1;%dm%s\033[0m" % (font, text)


class GameObject:
    """ base game object """
    indicating_char = ''        # what to indicate
    alive = True                # is alive, turn False if blood <= 0
    inside_cave = False
    cave = None
    cave_pos = None
    active = True

    def __init__(self, x, y, step_num, blood=10):
        """ assign values and put to board """
        self.x = x
        self.y = y
        self.step_num = step_num
        self.blood = self.orig_blood = blood
        self.on_board = False
        if not isinstance(objects[self.y][self.x], GameObject):
            self.on_board = True
            objects[self.y][self.x] = self
        else:
            print(color(31, "Position (%d, %d) already used." % (x + 1, 5 - y)))
            sleep(0.3)
        self.hanging_up_actions = [self.out_cave]

    def __str__(self):
        """ indicate """
        return self.indicating_char

    def __repr__(self):
        return str(self)

    def die(self):
        """ what to do when dying """
        pass

    def step(self, step_num):
        """ go pass 1 step """
        pass

    def cave_step(self, step_num):
        """ go pass 1 step in cave """
        pass

    def full_step(self, step_num):
        """ check everything """
        self.full_check()
        if self.alive and self.active:
            self.step(step_num) if not self.inside_cave else self.cave_step(step_num)

    def check(self):
        pass

    def full_check(self):
        if self.blood < 1:
            self.alive = False
        if not self.alive:
            objects[self.y][self.x] = 0
            self.die()
        if not self.active and self.alive:
            for action in self.hanging_up_actions:
                action()
        self.check()

    def into_cave(self, cave, pos):
        self.inside_cave = True
        self.cave = cave
        self.cave_pos = pos
        objects[self.y][self.x] = 0
        self.cave.inside[self.cave_pos] = self

    def out_cave(self):
        exit_hole = self.cave.exit_hole
        if not isinstance(objects[exit_hole.y][exit_hole.x - 1], GameObject):
            self.cave.inside[self.cave_pos] = 0
            self.active = True
            self.x = exit_hole.x - 1
            self.y = exit_hole.y
            objects[exit_hole.y][exit_hole.x - 1] = self
            self.inside_cave = False
            self.cave = None
            self.cave_pos = 0
        else:
            self.active = False


class Plant(GameObject):
    """ base plant """
    indicating_char_colorless = ''

    def __init__(self, x, y, step_num, sun_required, blood=10):
        """ different from base object: sunlight """
        global sunlight
        if sunlight >= sun_required:
            if x in range(9):
                super().__init__(x, y, step_num, blood)
                if self.on_board:
                    sunlight -= sun_required
            else:
                self.on_board = False
                print(color(31, "Position not available."))
                sleep(0.3)
        else:
            print(color(31, "Sunlight not enough."))
            sleep(0.3)
            self.on_board = False
        global all_plants
        all_plants += 1

        with open("current_grades.json", 'r') as fp:
            self.grade = json.load(fp)[self.indicating_char_colorless]

    def check(self):
        if not self.alive and self.blood == self.orig_blood - 50:
            objects[self.y][self.x] = color(31, '0')

    def die(self):
        global dead_plants
        dead_plants += 1

    def full_step(self, step_num):
        super().full_step(step_num)
        if self.grade > 0:
            for o in objects[self.y]:
                if isinstance(o, BaseZombie):
                    ga[self.indicating_char_colorless][self.grade](self, o)


class Sunflower(Plant):
    indicating_char = color(33, 's')
    indicating_char_colorless = 's'

    def __init__(self, x, y, step_num):
        super().__init__(x, y, step_num, 50)
        if self.on_board:
            print(color(33, ('Sunflower planted at (%d, %d), '
                             + 'costing 50 sunlight.')
                        % (self.x + 1, 5 - self.y)))
            sleep(0.3)

    def step(self, step_num):
        sep = r(2, 5)
        if step_num % sep == self.step_num % sep:
            global sunlight
            sunlight += 50
            print(color(33, ("50 sunlight produced by "
                  + "sunflower at (%d, %d).")
                  % (self.x + 1, 5 - self.y)))
        sleep(0.3)


class PeaShooter(Plant):
    indicating_char = color(32, 'p')
    indicating_char_colorless = 'p'

    def __init__(self, x, y, step_num):
        super().__init__(x, y, step_num, 100)
        if self.on_board:
            print(color(32, ('Peashooter planted at (%d, %d), '
                        + 'costing 100 sunlight.')
                        % (self.x + 1, 5 - self.y)))
            sleep(0.3)

    def step(self, step_num):
        for o in objects[self.y]:
            if isinstance(o, BaseZombie):
                o.blood -= 1
                print(color(32,
                            'Zombie at (%d, %d) attacked by peashooter at (%d, %d).'
                            % (o.x + 1, 5 - o.y, self.x + 1, 5 - self.y)))
                sleep(0.3)
                break


class Nut(Plant):
    indicating_char = color(36, 'n')
    indicating_char_colorless = 'n'

    def __init__(self, x, y, step_num):
        super().__init__(x, y, step_num, 50, 30)
        if self.on_board:
            print(color(36, ('Nut planted at (%d, %d), '
                             + 'costing 50 sunlight.')
                        % (self.x + 1, 5 - self.y)))
            sleep(0.3)


class BaseZombie(GameObject):
    def __init__(self, y, speed, harm, action, step_num, die_to_exit=False, blood=7):
        super().__init__(9, y, step_num, blood)
        self.speed = speed
        self.harm = harm
        self.die_to_exit = die_to_exit
        self.action = action
        global all_zombies
        all_zombies += 1

    def die(self):
        global dead_zombies
        dead_zombies += 1
        objects[self.y][self.x] = color(32, '0')
        '''if self.die_to_exit:
            global exited, plant_win
            exited = True
            plant_win = True'''

    def step(self, step_num):
        if self.x == 0:
            global exited, plant_win
            exited = True
            plant_win = False
        else:
            near = objects[self.y][self.x - 1]
            if isinstance(near, Plant):
                near.blood -= self.harm
                print(color(35, 'Zombie at (%d, %d) %s plant at (%d, %d).'
                            % (self.x + 1, 5 - self.y, self.action, self.x, 5 - self.y)))
                sleep(0.3)
            elif isinstance(objects[self.y][self.x - self.speed], GameObject):
                objects[self.y][self.x] = 0
                before_pos = self.x + 1
                self.x -= 1
                objects[self.y][self.x] = self
                print(color(35, "Zombie walked from %d to %d."
                            % (before_pos, self.x + 1)))
                sleep(0.3)
            else:
                objects[self.y][self.x] = 0
                before_pos = self.x + 1
                self.x -= self.speed
                objects[self.y][self.x] = self
                print(color(35, "Zombie walked from %d to %d."
                            % (before_pos, self.x + 1)))
                sleep(0.3)

    def cave_step(self, step_num):
        if self.cave_pos < 1:
            self.out_cave()
        else:
            pos_before = self.cave_pos
            self.cave_pos -= self.speed
            if self.cave_pos < 0:
                self.cave_pos = 0
            self.cave.inside[pos_before] = 0
            self.cave.inside[self.cave_pos] = self
            print(color(35, "Zombie in cave %s walked from %d to %d."
                        % (self.cave.cave_id, pos_before, self.cave_pos)))
            sleep(0.3)


class Zombie(BaseZombie):
    indicating_char = color(35, 'z')

    def __init__(self, y, step_num, die_to_exit=False):
        super().__init__(y, 1, 1, 'eating', step_num, die_to_exit)


class KickerZombie(BaseZombie):
    indicating_char = color(31, 'k')

    def __init__(self, y, step_num, die_to_exit=False):
        super().__init__(y, 1, 50, 'kicking', step_num, die_to_exit)


class DiggerZombie(BaseZombie):
    indicating_char = color(35, 'd')

    def __init__(self, y, step_num, die_to_exit=False):
        super().__init__(y, 1, 1, 'eating', step_num, die_to_exit)
        self.before_dig = r(1, 3)
        self.group = None

    def step(self, step_num):
        super().step(step_num)
        if step_num - self.step_num == self.before_dig:
            print(color(35, "I'm a digger zombie and I want to dig a "
                        + "hole. How would you name it (1 char)? "), end='')
            cave_id = input()
            import re
            while len(cave_id) != 1 or not re.match(r'[a-zA-Z]', cave_id):
                print(color(35, "Invalid input. Please enter again: "), end='')
                cave_id = input()
            self.group = CaveGroup(cave_id)
            self.into_cave(self.group, 4)
            CaveStart(self.x, self.y, step_num, self.group)

    def cave_step(self, step_num):
        if self.cave_pos < 1:
            x, y = self.group.start_hole.x, r(0, 4)
            while isinstance(objects[y][x], GameObject):
                x, y = self.group.start_hole.x, r(0, 4)
            CaveExit(x, y, step_num, self.group)
            self.out_cave()
        else:
            pos_before = self.cave_pos
            self.cave_pos -= self.speed
            if self.cave_pos < 0:
                self.cave_pos = 0
            self.cave.inside[pos_before] = 0
            self.cave.inside[self.cave_pos] = self
            print(color(35, "Zombie in cave %s walked from %d to %d."
                        % (self.cave.cave_id, pos_before, self.cave_pos)))
            sleep(0.3)


class CaveGroup:
    start_hole = None
    exit_hole = None
    inside = [0] * 5

    def __init__(self, cave_id):
        self.cave_id = cave_id
        caves[self.cave_id] = self


class CaveStart(GameObject):
    def __init__(self, x, y, step_num, parent: CaveGroup):
        super().__init__(x, y, step_num)
        if not parent.start_hole:
            parent.start_hole = self
        else:
            raise ValueError("This CaveGroup already has a start hole.")
        self.parent = parent
        self.indicating_char = color(34, self.parent.cave_id)

    def check(self):
        front = objects[self.y][self.x + 1]
        if isinstance(front, BaseZombie):
            front.into_cave(self.parent, 4)


class CaveExit(GameObject):
    def __init__(self, x, y, step_num, parent: CaveGroup):
        super().__init__(x, y, step_num)
        if not parent.exit_hole:
            parent.exit_hole = self
        else:
            raise ValueError("This CaveGroup already have an exit hole.")
        self.parent = parent
        self.indicating_char = color(36, self.parent.cave_id)
