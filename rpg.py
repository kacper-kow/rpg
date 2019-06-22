#!/bin/python3

# Replace RPG starter project with this code when new instructions are live
from random import random


def showInstructions():
    # print a main menu and the commands
    print('''
RPG Game
========
Commands:
  go [direction]
  get [item]
''')

# an inventory, which is initially empty
inventory = []

# health shows how much lives you have
health = 20

# mana shows how much magic power you have
mana = 0
# looks how strong you are
strength = 10

# what we have on
equipped = None

# a dictionary linking a room to other rooms
rooms = {
    'Hall': {
        'south': 'Library',
        'east': 'Wrought',
        'item': 'apple'

    },
    'Old Library': {
        'north': 'Hall',
        'item': 'key'
    },
    'Wrought': {
        'west': 'Hall',
        'monsters': ['green_slime', 'snake'],
        'item': 'broken sword'
    },
}
items = {
    'apple':
        {
            'can_eat': True,
            'can_equip': False,
            'health': 5,
        },
    'broken sword':
        {
            'can_eat': False,
            'can_equip': True,
            'strength': 5
        }
}


monsters = {
    'green_slime':
        {
            'health': 20,
            'attack': 5,
        },
    'snake':
        {
            'health': 15,
            'attack': 3,
        }
}

# start the player in the Hall
currentRoom = 'Hall'

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
    return userinput.split()[0], ' '.join(userinput.split()[1:])


def showStatus():
    # print the player's current status
    print('---------------------------')
    # print the player's current health and mana
    print('Health: {}, Mana: {}, strength: {}'.format(health, mana, strength))
    if equipped is not None:
        print('  equipped: {} {}'.format(equipped, items[equipped]['strength']))
    print('You are in the ' + currentRoom)
    # print the current inventory
    print('Inventory : ' + str(inventory))
    # print an item if there is one
    if "item" in rooms[currentRoom]:
        print('You see a ' + rooms[currentRoom]['item'])
    if 'monsters' in rooms[currentRoom]:
        for monster in rooms[currentRoom]['monsters']:
            print('A {} approaches'.format(monster))
    print("---------------------------")


# fight mode
def showFightStatus():
    # print the player's current status
    print('-------FIGHT MODE--------')
    # print the player's current health and mana
    print('Health: {}, Mana: {}'.format(health, mana))
    if 'monsters' in rooms[currentRoom]:
        for monster in rooms[currentRoom]['monsters']:
            print('A {} will fight against you(HP{})'.format(monster, monsters[monster]['health']))


def fight():
    global health
    global strength

    while True:
        showFightStatus()
        command, target = get_user_input()

        if command == 'flee':
            if random() > 0.5:
                print('You escaped safely. The monsters dissapeared.')
                del rooms[currentRoom]['monsters']
                break
            else:
                print('Your try to escape failed.')

        if command == 'attack':
            if target in monsters and target in rooms[currentRoom]['monsters']:
                if random() > 0.2:
                    print('The attack was successful')
                    monsters[target]['health'] -= strength
                elif random() > 0.8:
                    print('A critical Hit!')
                    monsters[target]['health'] -= strength * 2
                else:
                    print('The monster dodged your attack...')

        for monster in rooms[currentRoom]['monsters']:
            if monsters[monster]['health'] <= 0:
                print('The {} is defeated.'.format(monster))
                del monsters[monster]
                rooms[currentRoom]['monsters'].remove(monster)

        # leave the fight mode if no monsters left
        if len(rooms[currentRoom]['monsters']) == 0:
            del rooms[currentRoom]['monsters']
            return

        for monster in rooms[currentRoom]['monsters']:
            if random() > 0.3:
                print('The {} hits you!'.format(monster))
                health -= monsters[monster]['attack']
            elif random() > 0.9:
                print('The {} lands a critical hit!'.format(monster))
                health -= monsters[monster]['attack'] * 2
            else:
                print('You dodged an attack from the {}'.format(monster))
            if health <= 0:
                return


def remove_current_equipment():
    global strength, equipped
    if equipped is not None:
        print('You\'ve taken off your {}.'.format(equipped))
        strength -= items[equipped]['strength']
        equipment_strength = 0
        equipped = None
        inventory.add(target)


# loop forever
while True:
    if health <= 0:
        print('     -GAME OVER-     ')
        break

    showStatus()

    if 'monsters' in rooms[currentRoom]:
        fight()
        continue

    command, target = get_user_input()

    # if they type 'go' first
    if command == 'go':
        # check that they are allowed wherever they want to go
        if target in rooms[currentRoom]:
            # set the current room to the new room
            currentRoom = rooms[currentRoom][target]
        # there is no door (link) to the new room
        else:
            print('You can\'t go that way!')

    # if they type 'get' first
    if command == 'get':
        # if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and target in rooms[currentRoom]['item']:
            # add the item to their inventory
            inventory += [target]
            # display a helpful message
            print(target + ' got!')
            # delete the item from the room
            del rooms[currentRoom]['item']
        # otherwise, if the item isn't there to get
        else:
            # tell them they can't get it
            print('Can\'t get ' + target + '!')

    if command == 'eat':
        if target in inventory:
            if target in items and items[target]['can_eat']:
                health +=items[target]['health']
                inventory.remove(target)
                print('You eat the {}. {} HP recovered.'.format(target, items[target]['health']))
            else:
                print('Can\'t eat {}'.format(target))
        else:
            print('You don\'t have {}...'.format(target))

    if command == 'equip':
        if target in inventory:
            if target in items and items[target]['can_equip']:
                remove_current_equipment()
                print('You equipped the {}.'.format(target))
                strength += items[target]['strength']
                inventory.remove(target)
                equipped = target
            else:
                print('You can\'t equip {}'.format(target))
        else:
            print('You don\'t have {}'.format(target))

    if command == 'unequip':
        remove_current_equipment()

