#SERVER FUNCTIONS
import sys

cms = ["new", "help"]
descriptions = ["Introduction to the game.", "Advanced Help Menu."]


# NEW PLAYER
def new():
    return 'WELCOME TO CIRCLE!'


# HELP
def help():
    d = '\nHELP MENU \n'
    for (cm, description) in zip(cms, descriptions):
        d += f'{cm} \t\t\t {description}\n'
    return d