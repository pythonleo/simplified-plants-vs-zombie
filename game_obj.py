objects = [[0] * 10 for i in range(5)]    # game board
sunlight = 50                             # sunlight, initial value 50
exited = False                            # is game exiting
plant_win = False                         # is plants winning
all_plants = 0
dead_plants = 0
all_zombies = 0
dead_zombies = 0


def color(font, text):
    return "\033[1;%dm%s\033[0m" % (font, text)


class GameObject:
    """ base game object """
    indicating_char = ''        # what to indicate
    alive = True                # is alive, turn False if blood <= 0

    def __init__(self, x, y, blood=10):
        """ assign values and put to board """
        self.x = x
        self.y = y
        self.blood = self.orig_blood = blood
        self.on_board = False
        if not isinstance(objects[self.y][self.x], GameObject):
            self.on_board = True
            objects[self.y][self.x] = self
        else:
            print(color(31, "Position already used."))

    def __str__(self):
        """ indicate """
        return self.indicating_char

    def die(self):
        """ what to do when dying """
        pass

    def step(self, step_num):
        """ go pass 1 step """
        pass

    def full_step(self, step_num):
        """ check everything """
        self.full_check()
        if self.alive:
            self.step(step_num)

    def check(self):
        pass

    def full_check(self):
        if self.blood < 1:
            self.alive = False
        if not self.alive:
            objects[self.y][self.x] = 0
            self.die()
        self.check()


class Plant(GameObject):
    """ base plant """
    def __init__(self, x, y, sun_required):
        """ different from base object: sunlight """
        global sunlight
        if sunlight >= sun_required:
            if x in range(9):
                super().__init__(x, y)
                if self.on_board:
                    sunlight -= sun_required
            else:
                print(color(31, "Position not available."))
        else:
            print(color(31, "Sunlight not enough."))
            self.on_board = False
        global all_plants
        all_plants += 1

    def check(self):
        if not self.alive and self.blood == self.orig_blood - 30:
            objects[self.y][self.x] = color(31, '0')

    def die(self):
        global dead_plants
        dead_plants += 1


class Sunflower(Plant):
    indicating_char = color(33, 's')

    def __init__(self, x, y, step_num):
        super().__init__(x, y, 50)
        if self.on_board:
            self.step_num = step_num
            print(color(33, ('Sunflower planted at (%d, %d), '
                             + 'costing 50 sunlight.')
                        % (self.x + 1, 5 - self.y)))

    def step(self, step_num):
        if step_num % 3 == self.step_num % 3:
            global sunlight
            sunlight += 50
            print(color(33, ("50 sunlight produced by "
                  + "sunflower at (%d, %d).")
                        % (self.x + 1, 5 - self.y)))


class PeaShooter(Plant):
    indicating_char = color(32, 'p')

    def __init__(self, x, y):
        super().__init__(x, y, 100)
        if self.on_board:
            print(color(32, ('Peashooter planted at (%d, %d), '
                        + 'costing 100 sunlight.')
                        % (self.x + 1, 5 - self.y)))

    def step(self, step_num):
        for o in objects[self.y]:
            if isinstance(o, BaseZombie):
                o.blood -= 1.5
                print(color(32,
                            'Zombie at (%d, %d) attacked by peashooter at (%d, %d).'
                            % (o.x + 1, 5 - o.y, self.x + 1, 5 - self.y)))
                break


class BaseZombie(GameObject):
    def __init__(self, y, speed, harm, action, die_to_exit=False):
        super().__init__(9, y)
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
        if self.die_to_exit:
            global exited, plant_win
            exited = True
            plant_win = True

    def step(self, step_num):
        if self.x == 0:
            global exited, plant_win
            exited = True
            plant_win = False
        else:
            if isinstance(objects[self.y][self.x - 1], Plant):
                objects[self.y][self.x - 1].blood -= self.harm
                print(color(35, 'Zombie at (%d, %d) %s plant at (%d, %d).'
                            % (self.x + 1, 5 - self.y, self.action, self.x, 5 - self.y)))
            elif not isinstance(objects[self.y][self.x - 1], GameObject):
                objects[self.y][self.x] = 0
                before_pos = self.x + 1
                self.x -= self.speed
                objects[self.y][self.x] = self
                print(color(35, "Zombie walked from %d to %d."
                            % (before_pos, self.x + 1)))


class Zombie(BaseZombie):
    indicating_char = color(35, 'z')

    def __init__(self, y, die_to_exit=False):
        super().__init__(y, 1, 1, 'eating', die_to_exit)


class KickerZombie(BaseZombie):
    indicating_char = color(31, 'k')

    def __init__(self, y, die_to_exit=False):
        super().__init__(y, 1, 30, 'kicking', die_to_exit)
