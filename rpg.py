#!/bin/python3

# Replace RPG starter project with this code when new instructions are live
from random import random


def showInstructions():
  #print a main menu and the commands
  print('''
RPG Game
========
Commands:
  go [direction]
  get [item]
''')

def showStatus():
  #print the player's current status
  print('---------------------------')
  #print the player's current health and mana
  print('Health: {}, Mana: {}'.format(health, mana))
  print('You are in the ' + currentRoom)
  #print the current inventory
  print('Inventory : ' + str(inventory))
  if 'monsters' in rooms[currentRoom]:
      for monster in rooms[currentRoom]['monsters']:
          print ('A {} approaches'.format(monster))
  #print an item if there is one
  if "item" in rooms[currentRoom]:
    print('You see a ' + rooms[currentRoom]['item'])
  print("---------------------------")

#an inventory, which is initially empty
inventory = []

#health shows how much lives you have
health = 20

#mana shows how much magic power you have
mana = 0



#a dictionary linking a room to other rooms
rooms = {
    'Hall' : {
        'south' : 'Kitchen',
        'east'  : 'Dining Room',
        'item'  : 'apple'

    },
    'Kitchen' : {
        'north' : 'Hall',
        'item': 'key'
    },
    'Dining Room': {
        'west': 'Hall',
        'monsters': ['green_slime', 'frog']
    },
}

monsters = {
    'green_slime':
        {
            'health': 20,
            'attack': 10,
        },
    'frog':
        {
            'health': 15,
            'attack': 10,
        }
}


#start the player in the Hall
currentRoom = 'Dining Room'

showInstructions()


def get_user_input():
    # get the player's next 'move'
    # .split() breaks it up into an list array
    # eg typing 'go east' would give the list:
    # ['go','east']
    userinput = ''
    while userinput == '':
        userinput = input('>')
    userinput = userinput.lower()
    return userinput.split()

#fight mode
def showFightStatus():
    # print the player's current status
    print('-------FIGHT MODE--------')
    # print the player's current health and mana
    print('Health: {}, Mana: {}'.format(health, mana))
    if 'monsters' in rooms[currentRoom]:
        for monster in rooms[currentRoom]['monsters']:
            print ('A {} will fight against you(HP{})'.format(monster, monsters[monster]['health']))




def fight():
    while True:
        showFightStatus()
        move = get_user_input()

        if move[0] == 'flee':
            if random() > 0.5:
                print('You escaped safely. The monsters dissapeared.')
                del rooms[currentRoom]['monsters']
                break
            else:
                print('Your try to escape failed.')

        if move [0] == 'attack':

            if move[1] in monsters and move[1] in rooms[currentRoom]['monsters']:
                if random() > 0.2:
                    print('The attack was successful')
                    monsters[move[1]]['health'] -= 10
                elif random() > 0.8:
                    print('A critical Hit!')
                    monsters[move[1]]['health'] -= 20
                else:
                    print('The monster dodged your attack...')

        for monster in rooms [currentRoom]['monsters']:
            if monsters [monster]['health']<=0:
                print('The {} is defeated.'.format(monster))
                del monsters[monster]
                rooms[currentRoom]['monsters'].remove(monster)










#loop forever
while True:
    showStatus()

    if 'monsters' in rooms[currentRoom]:
        fight()
        continue



    move = get_user_input()

    #if they type 'go' first
    if move[0] == 'go':
        #check that they are allowed wherever they want to go
        if move[1] in rooms[currentRoom]:
            #set the current room to the new room
            currentRoom = rooms[currentRoom][move[1]]
        #there is no door (link) to the new room
        else:
            print('You can\'t go that way!')

    #if they type 'get' first
    if move[0] == 'get' :
        #if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
            #add the item to their inventory
            inventory += [move[1]]
            #display a helpful message
            print(move[1] + ' got!')
            #delete the item from the room
            del rooms[currentRoom]['item']
    #otherwise, if the item isn't there to get
    else:
        #tell them they can't get it
        print('Can\'t get ' + move[1] + '!')

    if move[0] == 'eat':
        if move[1] in inventory:
            if move[1] == 'apple':
                health += 5
                inventory.remove('apple')
                print('You eat an Apple. 5 HP recovered.')
            else:
                print('Can\'t eat {}'.format(move[1]))
        else:
            print('You don\'t have {}...'.format(move[1]))

