import game_obj as o


upgrade_levels = {
    2: [{'p': 1, 's': 0, 'n': 0},
        {"Peashooter": 2}],
    3: [{'s': 1, 'p': 1, 'n': 0},
        {"Sunflower": 2}],
    4: [{'p': 2, 'n': 1, 's': 1},
        {"Peashooter": 3, "Nut": 2}],
    5: [{'s': 2, 'n': 2, 'p': 2},
        {"Sunflower": 3, "Nut": 3}]
}


# Peashooter
def five_peas(self, z):
    if o.r(1, 5) == 1:
        print(o.color(32, "Grade 2 peashooter's Five Peas!"))
        o.sleep(.3)
        print(o.color(32, "Zombie at (%d, %d) attacked by five peas from (%d, %d)!"
                      % (z.x + 1, 5 - z.y, self.x + 1, 5 - self.y)))
        o.sleep(.3)
        z.blood -= 5


def ten_peas(self, z):
    if o.r(1, 5) == 1:
        print(o.color(32, "Grade 3 peashooter's Ten Peas!"))
        o.sleep(.3)
        print(o.color(32, "Zombie at (%d, %d) attacked by ten peas from (%d, %d)!"
                      % (z.x + 1, 5 - z.y, self.x + 1, 5 - self.y)))
        o.sleep(.3)
        z.blood -= 10


# Sunflower
def ultra_sunlight(self, z):
    if o.r(1, 7) == 1:
        print(o.color(33, "Grade 2 Sunflower's Ultra Sunlight!"))
        o.sleep(.3)
        print(o.color(33, "100 sunlight was added by sunflower at (%d, %d)!"
                      % (self.x + 1, 5 - self.y)))
        o.sleep(.3)
        o.sunlight += 100


def sunlight_burn(self, z):
    if o.r(1, 10) == 1:
        print(o.color(33, "Grade 3 Sunflower's Sunlight Burn!"))
        o.sleep(.3)
        print(o.color(33, "Zombie at (%d, %d) attacked by reflected sunlight from (%d, %d)!"
                      % (z.x + 1, 5 - z.y, self.x + 1, 5 - self.y)))
        o.sleep(.3)
        print(o.color(33, "100 sunlight was added by sunflower at (%d, %d)!"
                      % (self.x + 1, 5 - self.y)))
        o.sleep(.3)
        z.blood -= 5
        o.sunlight += 100


# Nut
def metal_shell(self, z):
    if o.r(1, 5) == 1 and z.x - 1 == self.x:
        print(o.color(36, "Grade 2 Nut's Metal Shell!"))
        o.sleep(.3)
        print(o.color(36, "The zombie at (%d, %d) cannot eat the Nut at (%d, %d) in this round!"
                      % (z.x + 1, 5 - z.y, self.x + 1, 5 - self.y)))
        o.sleep(.3)
        self.blood += 1


def body_hit(self, z):
    if o.r(1, 10) == 1 and z.x - 1 == self.x:
        print(o.color(36, "Grade 3 Nut's Body Hit!"))
        o.sleep(.3)
        print(o.color(36, "The zombie in front is hit by the body of Nut at (%d, %d)!"
                      % (self.x + 1, 5 - self.y)))
