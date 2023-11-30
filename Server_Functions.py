#SERVER FUNCTIONS
import sys
import os

cms = ["new", "help", "playerlist"]
descriptions = ["\t Introduction to the game.", "\t Advanced Help Menu.", "\t Player List."]


# NEW PLAYER
def new():
    d=''
    d += f'\nWe to the CIRCLE! \n'
    d += f'In Circle, you will see a group of people who suddenly find themselves in a dark room. They are all strangers, and they are all trapped. \n'
    d += f'Every round, You MUST vote off 1 person. \n'
    d += f'If you are voted off, you are eliminated from the game and thus from real life. \n'
    d += f'If you are the last person standing, you live. \n'
    d += f'The Question is, Who deserves to live? \n'
    d += f'Type --join to join a private game, or create one by using --create \n'
    d += f'Please wait for the admin to start the game. \n'
   
    return d


# HELP
def help():
    d=(f"\n******************************************\n")
    d += '\nHELP MENU \n'
    for (cm, description) in zip(cms, descriptions):
        d += f'{cm} \t\t\t {description}\n'
    d+=(f"\n******************************************\n")
    return d