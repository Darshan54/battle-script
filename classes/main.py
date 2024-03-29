from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# creating black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# creating white magics
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# creating items
potion = Item("Potion", "potion", "Heals for 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals for 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals for 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 Damage", 500)


player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

player1 = Person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick: ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Imp  :", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus:", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp  :", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
'''
for i in range(4):
    print(player.generate_damage())
'''

# player.choose_magic()

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("===============")

    print("\n")
    print("NAME                         HP                                         MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("     Choose Action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ","") + " for ", dmg, " points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ","") + "has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("     Choose Magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for ", magic_dmg, " HP." + bcolors.ENDC)

            elif spell.type == "black":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", magic_dmg, " points of damage to " + enemies[enemy].name.replace(" ","") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","") + "has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("     Choose Item:")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "None Left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for ", str(item.prop), " HP" + bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + "fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + "deals ", str(item.prop), " points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","") + " has died.")
                    del enemies[enemy]

        remaining_enemy = 0
        for enemy in enemies:
            remaining_enemy += 1

        # check if player won
        if remaining_enemy == 0:
            print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
            running = False
            break      #end battle


    #Enemy attack phase
    print("\n")

    for enemy in enemies:
        #if enemy.mp > min(spell.cost) then only give option,else attack compulsary
        mini = enemy.magic[0].cost
        for spell in enemy.magic:
            if spell.cost <= mini:
                mini = spell.cost

        if enemy.get_mp() >= mini:
            enemy_choice = random.randrange(0,2)
        else:
            enemy_choice = 0

        #chose attack
        if enemy_choice == 0:
            target = random.randrange(0,len(players))
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ","") + " attacked " + players[target].name.replace(" ","") + " for", enemy_dmg)

        elif enemy_choice == 1:
           spell, magic_dmg = enemy.choose_enemy_spell()
           enemy.reduce_mp(spell.cost)

           if spell.type == "white":
               enemy.heal(magic_dmg)
               print(bcolors.OKBLUE + "\n" + spell.name + "heals " + enemy.name + " for ", magic_dmg, " HP." + bcolors.ENDC)

           elif spell.type == "black":

               target = random.randrange(0,len(players))

               players[target].take_damage(magic_dmg)

               print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", magic_dmg,
                     " points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)


        #deleting died players
        i = -1
        for player in players:
            i += 1
            if player.get_hp() == 0:
               print(players[i].name.replace(" ", "") + " has died.")
               del players[i]


        # check if Enemy won
        remaining_player = 0
        for player in players:
            remaining_player += 1

        if remaining_player == 0:
            print(bcolors.FAIL + bcolors.BOLD + "You Enemies have Defeated You!" + bcolors.ENDC)
            running = False
            break  # end battle
