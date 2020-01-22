from game_props import *
import colorama
colorama.init()
choice = ''


def instruct():
    print("Here's the instructions about the game.")
    print("Press " + o.color(31, '<ENTER>') + " after you read each instruction.\n"
          + "Here they are!")
    print("In this game, you're going to fight against "
          + "the zombies with your...plants!")
    input()
    print("You have 3 kinds of plants: " + o.color(33, "sunflowers")
          + ", " + o.color(32, "peashooters") + " and " + o.color(36, 'nuts') + ".")
    input()
    print("Everything works in " + o.color(36, "a 10*5 grid")
          + " in this game. And things will change step by step.")
    input()
    print("Meanings of the output:\nYou need 'sunlight' to plant plants."
          + "A sunflower needs 50 sunlight and 100 for a peashooter.\n"
          + "'Current state' outputs the current game grid, "
          + "where " + o.color(33, "'s'") + " means a "
          + o.color(33, "sunflower") + ", " + o.color(32, "'p'")
          + " stands for a " + o.color(32, "peashooter")
          + ", " + o.color(36, "'n'") + "is a " + o.color(36, "nut")
          + ", " + o.color(35, "'z'") + " symbolizes a "
          + o.color(35, "zombie") + " and '0' is an "
          + o.color(36, "empty grid") + ". "
          + "And the 'next step' prompt wants you to enter a command "
          + "for the next step (press " + o.color(31, '<ENTER>')
          + " if you don't want to do anything) .")
    input()
    print("For example:\nSunlight: 50.\nCurrent state:\n" + ('0  ' * 10 + '\n') * 5
          + "\nThat means you have 50 sunlight and an empty grid.")
    input()
    print("Plant your plants using 'plant type x y' commands "
          + "in the 'next step' prompt, "
          + "in which 'type' means the type of the plant "
          + "(s for " + o.color(33, "sunflower")
          + " and p for " + o.color(32, "peashooter") + "), "
          + "'x' means the position you want to plant it on the x-axis"
          + "(starting with 1 from left to right), "
          + "and 'y' is the position on the y-axis "
          + "(starting with 1 from down to up).")
    input()
    print("For example:\nnext step: plant s 1 1\n"
          + "That means to plant a sunflower on the down-left corner grid.")
    input()
    print("So how do your plants " + o.color(31, "fight")
          + " with the " + o.color(35, "zombies") + "?\n"
          + "As you can see, planting plants needs sunlight. "
          + "But only 50 sunlight is given. So you need "
          + o.color(33, "sunflowers") + " to produce sunlight for you. "
          + "A sunflower produces 50 sunlight every 2 to 5 step.\n"
          + o.color(32, "Peashooters") + " are real fighters. "
          + "A peashooter attacks the nearest zombie in front of it "
          + "every step. The zombie will die after a few steps. "
          + "A dead zombie will leave a green " + o.color(32, "'0'")
          + " in the place where it used to be.\n"
          + o.color(36, "Nuts") + " come in handy when you just want a shield. "
          + "They don't cost much (just 50 sunlight), but they are really strong. "
          + "It'd take a normal zombie 30 steps to eat all of one nut. "
          + "They save other plants loads of time to fight.")
    input()
    print("Ahh! A plant is planted in " + o.color(31, "a wrong position")
          + ". In this case, you can remove it by using 'remove x y' "
          + "commands in the 'next step' prompt, where 'x' and 'y' is the "
          + "position of the plant you want to remove, just like that in the plant command. "
          + "But the sunlight won't be returned to you. So, think it over before you "
          + "plant something.")
    input()
    print("Oh, look! What's that " + o.color(31, "'k'") + "? "
          + "Don't worry. It's just an evolved zombie that can 'kick' "
          + "your plant as it comes in front of it, and leave a red "
          + o.color(31, "'0'") + " in the place where the plant used to be. "
          + "So, be sure to kill it as soon as you can. ")
    input()
    print("And also, the zombie represented by " + o.color(35, "'d'") + " can dig a hole "
          + "and get in it. When he asks you for a name of the hole, don't refuse "
          + "to answer -- he will just stick to you before you give a good name. ")
    input()
    print("No more instructions! The world of Plants vs. Zombies is full of new surprises "
          + "for you to explore! (Hint: your plants might get stronger along the way...)")
    input()


def get_choice():
    global choice
    print("Enter 'i' to read the %s." % o.color(34, "instructions"))
    print("Enter 'p' to %s %s %s." % (
        o.color(31, "play"),
        o.color(33, 'the'),
        o.color(32, 'game')
    ))
    print("And press %s at any time you want to exit the game.\n"
          % o.color(31, "<Ctrl-C>"))
    try:
        choice = input("Make your choice: ")
        print()
    except KeyboardInterrupt:
        print(o.color(31, "Are you sure you want to exit? (y/n, default=n) "), end='')
        choice_exit = input()
        if choice_exit == 'y':
            import sys
            sys.exit()
        else:
            choice = input("Make your choice: ")
            print()


print("Welcome to the simplified " + o.color(32, "Plants")
      + " vs. " + o.color(35, "Zombie") + " game!\n")
print("You have several %s.\n" % o.color(36, "choices"))
while True:
    get_choice()
    try:
        if choice == 'i':
            instruct()
        elif choice == 'p':
            Game().start()
        else:
            print(o.color(31, "Invalid choice."))
    except KeyboardInterrupt:
        print(o.color(31, "Are you sure you want to exit? (y/n, default=n) "), end='')
        is_exit = input()
        if is_exit == 'y':
            import sys
            sys.exit()
        elif is_exit == 'n':
            get_choice()
