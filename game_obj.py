objects = [0] * 10
sunlight = 50
exited = False
plant_win = False


def color(mode, font, text):
    return "\033[%d;%dm%s\033[0m" % (mode, font, text)


class GameObject:
    indicating_char = ''
    blood = 10
    alive = True

    def __init__(self, pos):
        self.pos = pos
        if objects[self.pos] == 0:
            objects[self.pos] = self
        else:
            print(color(1, 31, "Position already used."))

    def __str__(self):
        return self.indicating_char

    def die(self):
        pass

    def step(self, step_num):
        pass

    def full_step(self, step_num):
        if self.blood < 1:
            self.alive = False
        if self.alive:
            self.step(step_num)
        else:
            self.die()
            objects[self.pos] = 0


class Plant(GameObject):
    def __init__(self, pos, sun_required):
        global sunlight
        if sunlight >= sun_required:
            if pos in range(9):
                super().__init__(pos)
            else:
                print(color(1, 31, "Position not available."))
            sunlight -= sun_required
        else:
            print(color(1, 31, "Sunlight not enough."))


class Sunflower(Plant):
    indicating_char = 's'

    def __init__(self, pos, step_num):
        super().__init__(pos, 50)
        self.step_num = step_num

    def step(self, step_num):
        if step_num % 2 == self.step_num % 2:
            global sunlight
            sunlight += 50


class PeaShooter(Plant):
    indicating_char = 'p'

    def __init__(self, pos):
        super().__init__(pos, 100)

    def step(self, step_num):
        for o in objects:
            if type(o) == Zombie:
                o.blood -= 1.5


class BaseZombie(GameObject):
    def __init__(self, speed, harm, die_to_exit=False):
        super().__init__(9)
        self.speed = speed
        self.harm = harm
        self.die_to_exit = die_to_exit

    def die(self):
        if self.die_to_exit:
            global exited, plant_win
            exited = True
            plant_win = True

    def step(self, step_num):
        if self.pos == 0:
            global exited, plant_win
            exited = True
            plant_win = False
        else:
            if isinstance(objects[self.pos - 1], Plant):
                objects[self.pos - 1].blood -= self.harm
            else:
                objects[self.pos] = 0
                if objects[self.pos - self.speed] == 0:
                    self.pos -= self.speed
                    objects[self.pos] = self
                else:
                    objects[self.pos - 1].blood -= 1


class Zombie(BaseZombie):
    indicating_char = 'z'

    def __init__(self, die_to_exit=False):
        super().__init__(1, 1, die_to_exit)
