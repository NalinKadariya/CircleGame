#SERVER FUNCTIONS
import sys

cms = ["new", "help", "join", "create"]
descriptions = ["Introduction to the game.", "Advanced Help Menu.", "Join a game.", "Create a game."]


# NEW PLAYER
def new():
    return 'WELCOME TO CIRCLE!'


# HELP
def help():
    d=(f"\n******************************************\n")
    d += '\nHELP MENU \n'
    for (cm, description) in zip(cms, descriptions):
        d += f'{cm} \t\t\t {description}\n'
    d+=(f"\n******************************************\n")
    return d


def join():
    return 'JOINING GAME.....'

def create():
    return 'CREATING GAME....'