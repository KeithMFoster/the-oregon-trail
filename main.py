import random
import builtins
import time
import keyboard


def setup():
    # set up the variables to be used in game
    game_variables = {
        # Identification of variables in the program
        # amount spent on animals
        "animals": 0,
        # amount spent on ammunition
        "ammunition": 0,
        # amount spent on clothing
        "clothing": 0,
        # flag for insufficient clothing in cold weather
        "insufficient_clothing": False,
        # counter in generating events
        "event_counter": 0,
        # turn number for setting date
        "game_turn": 0,
        # choice of shooting expertise level
        "shooting_expert_level": 0,
        # choice of eating
        "eating_choice": 0,
        # amount spent on food
        "food": 0,
        # flag for clearing south pass
        "south_pass_flag": False,
        # flag for injury
        "injury": False,
        # flag for blizzard
        "blizzard": False,
        # total mileage whole trip
        "mileage": 0,
        # amount spent on miscellaneous supplies
        "supplies": 0,
        # total mileage up through previous turn
        "turn_mileage": 0,
        # flag for clearing south pass in setting mileage
        "South_Pass_Mileage_Flag": False,
        # flag for illness
        "illness": False,
        # cash in your wallet
        "cash": 700,
        # flag for fort option
        "fort_flag": False
    }
    return game_variables


def shooting():
    print("\nYou pull your gun, aim, and pull the trigger")
    start_time = time.time()
    seconds = 15
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > seconds:
            print("Pop")
            my_score = 5
            break
        if keyboard.is_pressed(" "):
            if elapsed_time < 1:
                print("Wham!")
                my_score = 1
            elif elapsed_time < 2:
                print("POW!")
                my_score = 2
            elif elapsed_time < 4:
                print("Blam!")
                my_score = 3
            else:
                print("Bang")
                my_score = 4
            break
    return my_score


def illness(game_variables):
    if random.randint(1, 100) < 10 + 35 * (game_variables["eating_choice"] - 1):
        print("Wild Illness - Medicine Used.")
        game_variables["mileage"] = game_variables["mileage"] - 5
        game_variables["supplies"] = game_variables["supplies"] - 2
    elif random.randint(1, 100) < 100 - (40 / 4 ** (game_variables["eating_choice"] - 1)):
        print("Bad Illness - Medicine Used.")
        game_variables["mileage"] = game_variables["mileage"] - 5
        game_variables["supplies"] = game_variables["supplies"] - 5
    else:
        print("Serious Illness - You must stop for Medical Attention.")
        game_variables["illness"] = False
        game_variables["supplies"] = game_variables["supplies"] - 10

    # I'm sorry, but you don't have any more supplies.
    if game_variables["supplies"] < 10:
        dying("no_supplies")

    # There was a blizzard so let's return to it...
    if game_variables["blizzard"] == 1:
        return game_variables

    return game_variables


def mountains(game_variables):
    # Are you in the mountains?
    mountain_check = 9 - ((game_variables["mileage"] / 100 - 15) ** 2 + 72) / (
            (game_variables["mileage"] / 100 - 15) ** 2 + 12)

    # A check to see if you have been caught in the mountains or not.
    if random.randint(1, 10) > mountain_check:
        # Congratulations you have found your self in the mountains.
        if game_variables["south_pass_flag"]:
            game_variables["south_pass_flag"] = True

            # Is there a blizzard in the mountains? If, there is a loop until the weather clears.
            if random.randint(1, 100) < 81:
                print("You have been caught in a Blizzard in the Mountain Pass - Time and Supplies lost.")
                blizzard(game_variables)

            else:
                print("You made it safely through the South Pass -- No Snow")
                if game_variables["mileage"] < 1700:
                    game_variables["South_Pass_Mileage_Flag"] = True
                    return game_variables

        else:
            print("\nYou find yourself in some rugged mountains.")
            game_variables["mileage"] = game_variables["mileage"] - 60

            # let's check to see if you have been caught in a blizzard or not. For the rugged mountains, the chance is
            # only 33%
            if random.randint(1, 100) < 34:
                print("You have been caught in a Blizzard in the Mountain Pass - Time and Supplies lost.")
                blizzard(game_variables)
            elif random.randint(1, 100) > 10:
                print("\nWagon Damaged! - Lose time and supplies.\nThe going gets slow.")
                game_variables["supplies"] = game_variables["supplies"] - 5
                game_variables["ammunition"] = game_variables["ammunition"] - 200
                game_variables["clothing"] = game_variables["clothing"] - (random.randint(1, 40))
                game_variables["mileage"] = game_variables["mileage"] - 30 - (random.randint(1, 40))
            elif random.randint(1, 100) > 10:
                print("\nYou got lost - lose valuable time trying to find the trail!")
                game_variables["mileage"] = game_variables["mileage"] - 60
    return game_variables


def blizzard(game_variables):
    # Here is a loop that will run until the weather clears. There is a 20% chance that this might happen.
    base_chance_of_blizzard_over = 20
    while True:
        print("\nThe Snow and wind continues to rage.")
        game_variables["blizzard"] = True
        game_variables["food"] = game_variables["food"] - 25
        game_variables["supplies"] = game_variables["supplies"] - 10
        game_variables["ammunition"] = game_variables["ammunition"] - 300
        game_variables["mileage"] = game_variables["mileage"] - 30 - (random.randint(1, 40))

        # This is where  we will check to see if you have enough clothing to survive the blizzard.
        if game_variables["clothing"] < 18 + random.randint(1, 3):
            game_variables = illness(game_variables)

        # Did the weather clear?
        if random.randint(1, 100) < base_chance_of_blizzard_over:
            print("\nHurray! The Snow and wind start to break.")
            break

        # every cycle, lets add 10 percent chance that the blizzard is over.
        base_chance_of_blizzard_over = base_chance_of_blizzard_over + 10

        if game_variables["mileage"] < 1000:
            print("\nThrough the wind and snow, you finally make it out of the mountains. But the wrong side.")
            break

        # You ran out of food, sorry.
        if game_variables["food"] < 0:
            game_variables["food"] = 0
            dying("no_food")

        # You also ran out of supplies.
        if game_variables["supplies"] < 0:
            game_variables["supplies"] = 0
            dying("no_supplies")

        # slow down the loop, so it is readable for the user.
        time.sleep(5)
    return game_variables


def dying(reason):
    if reason != "":
        if reason == "no_food":
            print("You ran out of food and starved to death.")
        elif reason == "no_doctor":
            print("You can't afford a doctor.")
        elif reason == "no_supplies":
            print("You ran out of medical supplies")
        elif reason == "injury":
            # mishap = "pneumonia."
            mishap = "injuries."
            print("You died of " + mishap)

    print("Due to your unfortunate situation, there are a few")
    print("formalities we must go through\n")
    print("Would you like a minister?")
    print("Would you like a fancy funeral?")
    print("Would you like us to inform your next of kin?")

    print("But your Aunt Sadie in St. Louis is really worried about you.")

    print("That will be $4.50 for the telegraph charge.\n")
    print("We thank you for this information and we are sorry you")
    print("didn't make it to the great territory of Oregon")
    print("Better luck next time.\n\n")
    print("\tSincerely,")
    print("\tThe Oregon City Chamber of Commerce")


def buying_routine(object_name, min_amount, max_amount, wallet):
    my_purchase = 0
    while True:
        try:
            my_purchase = int(builtins.input(
                "Wallet: " + str(wallet) + ". How much do you want to spend on your " + object_name + ": "))
        except ValueError:
            print("Sorry, I didn't understand that.")
        if my_purchase < min_amount:
            print("Sorry, that is not enough.")
            continue
        elif my_purchase > max_amount:
            print("Sorry, that is too much.")
            continue
        elif my_purchase > wallet:
            print("You don't have that much - keep your spending down.")
        else:
            break
    return my_purchase


def initial_purchases(game_variables):
    # Oxen Team
    oxen = buying_routine("oxen team", 200, 300, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - oxen
    # food
    food = buying_routine("food", 1, 99999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - food

    # ammo
    ammo = buying_routine("ammunition", 1, 99999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - ammo

    # clothing
    clothing = buying_routine("clothing", 1, 99999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - clothing

    # miscellaneous supplies
    misc = buying_routine("miscellaneous supplies", 1, 99999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - misc

    total = 700 - oxen - clothing - ammo - food - misc
    if total < 0:
        print("You Overspent -- You only had $700 to spend. Try Again.")
        initial_purchases(game_variables)

    ammo = ammo * 50
    print("After all your purchases. You now have %d dollars left." % total)

    game_variables["cash"] = total
    game_variables["animals"] = oxen
    game_variables["ammunition"] = ammo
    game_variables["clothing"] = clothing
    game_variables["food"] = food
    game_variables["supplies"] = misc

    return game_variables


def instructions():
    print("This program simulates a trip over the oregon trail from Independence,")
    print("Missouri to Oregon City, Oregon in 1847 your family of five will cover")
    print("the 2040 mile Oregon Trail in 5-6 months --- if you make it alive.\n")
    print("You had saved $900 to spend for the trip, and you've just paid $200 for a wagon.")
    print("You will need to spend the rest of your money on the following items:\n")
    print("     Oxen - you can spend $200-$300 on your team")
    print("            the more you spend, the faster you'll go")
    print("            because you'll have better animals\n")
    print("     Food - the more you have, the less chance there")
    print("            is of getting sick\n")
    print("     Ammunition - $1 buys a belt of 50 bullets")
    print("            you will need bullets for attacks by animals")
    print("            and bandits, and for hunting food\n")
    print("     Clothing - this is especially important for the cold")
    print("            weather you will encounter when crossing")
    print("            the mountains\n")
    print("     Miscellaneous supplies - this includes medicine and")
    print("            other things you will need for sickness and")
    print("            emergency repairs\n\n")
    print("You can spend all your money before you start your trip -")
    print("or you can save some of your cash to spend at forts along")
    print("the way when you run low. However, items cost more at")
    print("the forts. You can also go hunting along the way to get")
    print("more food.\n")
    print("Whenever you have to use your trusty rifle along the way,")
    print("you will be told to type in a word (one that sounds like a ")
    print("gun shot). the faster you type in that word and hit the")
    print("'return' key, the better luck you'll have with your gun.\n")
    print("at each turn, all items are shown in dollar amounts")
    print("except bullets")
    print("when asked to enter money amounts, don't use a ""$"".\n")
    print("good luck!!!")


def user_stats(game_variables):
    # If any of the variables are below zero, we will set them to zero here.
    if game_variables["food"] < 0:
        game_variables["food"] = 0
    if game_variables["ammunition"] < 0:
        game_variables["ammunition"] = 0
    if game_variables["clothing"] < 0:
        game_variables["clothing"] = 0
    if game_variables["supplies"] < 0:
        game_variables["supplies"] = 0
    if game_variables["cash"] < 0:
        game_variables["cash"] = 0

    print("Food:            % d" % game_variables["food"])
    print("Bullets:         % d" % game_variables["ammunition"])
    print("Clothing:        % d" % game_variables["clothing"])
    print("Misc. Supplies:  % d" % game_variables["supplies"])
    print("Cash:            % d" % game_variables["cash"])
    return


def final_turn(game_variables):
    print("\nYou finally arrived at Oregon City\nafter 2040 long miles - Hooray!!\nA Real Pioneer!")
    time_calculation = (2040 - game_variables["turn_mileage"]) / (
                game_variables["mileage"] - game_variables["turn_mileage"])
    game_variables["food"] = game_variables["food"] + (1 - time_calculation) * (8 + 5 * game_variables["eating_choice"])

    time_calculation = int(time_calculation * 14)
    game_variables["game_turn"] = game_variables["game_turn"] * 14 + time_calculation

    if time_calculation < 0:
        time_calculation = 0

    if time_calculation > 7:
        time_calculation = 6

    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    the_day = days_list[time_calculation]

    if game_variables["game_turn"] < 124:
        game_variables["game_turn"] = game_variables["game_turn"] - 93
        print(the_day + ", July " + str(game_variables["game_turn"]) + ", 1847")
    elif game_variables["game_turn"] < 155:
        game_variables["game_turn"] = game_variables["game_turn"] - 124
        print(the_day + ", August " + str(game_variables["game_turn"]) + ", 1847")
    elif game_variables["game_turn"] < 185:
        game_variables["game_turn"] = game_variables["game_turn"] - 155
        print(the_day + ", September " + str(game_variables["game_turn"]) + ", 1847")
    elif game_variables["game_turn"] < 216:
        game_variables["game_turn"] = game_variables["game_turn"] - 185
        print(the_day + ", October " + str(game_variables["game_turn"]) + ", 1847")
    elif game_variables["game_turn"] < 246:
        game_variables["game_turn"] = game_variables["game_turn"] - 216
        print(the_day + ", November " + str(game_variables["game_turn"]) + ", 1847")
    else:
        game_variables["game_turn"] = game_variables["game_turn"] - 246
        print(the_day + ", December " + str(game_variables["game_turn"]) + ", 1847")

    user_stats(game_variables)
    print("\tPresident James K. Polk sends you his\n\theartiest congratulations")
    print("\tAnd wishes you a prosperous life ahead\n\tat you new home.")


def game_loop(game_variables):
    input_x = 0
    if game_variables["food"] < 0:
        game_variables["food"] = 0

    if game_variables["ammunition"] < 0:
        game_variables["ammunition"] = 0

    if game_variables["clothing"] < 0:
        game_variables["clothing"] = 0

    if game_variables["supplies"] < 0:
        game_variables["supplies"] = 0

    if game_variables["food"] < 13:
        print("\n\nYou'd better do some hunting or buy food and soon!!!!")

    game_variables["food"] = int(game_variables["food"])
    game_variables["ammunition"] = int(game_variables["ammunition"])
    game_variables["clothing"] = int(game_variables["clothing"])
    game_variables["supplies"] = int(game_variables["supplies"])
    game_variables["cash"] = int(game_variables["cash"])
    game_variables["mileage"] = int(game_variables["mileage"])

    game_variables["turn_mileage"] = game_variables["mileage"]

    if game_variables["illness"] or game_variables["injury"]:
        game_variables["cash"] = game_variables["cash"] - 20
        game_variables["illness"] = False
        game_variables["injury"] = False
        if game_variables["cash"] < 0:
            dying("no_doctor")
        print("Doctor's Bill is $20.")

    if game_variables["South_Pass_Mileage_Flag"]:
        print("Total Mileage:   950")
    else:
        print("Total Mileage:   % d" % game_variables["mileage"])
    user_stats(game_variables)

    if not game_variables["fort_flag"]:
        while True:
            try:
                input_x = int(builtins.input("\nDo you want to (1) Hunt, or (2) Continue: "))
            except ValueError:
                print("Sorry, I didn't understand that.")
            if input_x < 1 or input_x > 2:
                input_x = 3
                break
            elif input_x == 2 and game_variables["ammunition"] < 39:
                print("TOUGH -- You need more bullets to go hunting.")
            else:
                game_variables["fort_flag"] = True
                input_x = input_x + 1
                break
    else:
        while True:
            try:
                input_x = int(builtins.input("\nDo you want to (1) Stop at the next fort, (2) Hunt, or (3) Continue: "))
            except ValueError:
                print("Sorry, I didn't understand that.")
            if input_x < 1 or input_x > 3:
                input_x = 3
                break
            elif input_x == 2 and game_variables["ammunition"] < 39:
                print("TOUGH -- You need more bullets to go hunting.")
            else:
                break

    if input_x == 1:
        game_variables = fort(game_variables)
    elif input_x == 2:
        game_variables = hunting(game_variables)

    if game_variables["food"] < 14:
        dying("no_food")
    while True:
        try:
            input_x = int(builtins.input("Do you want to eat (1) Poorly, (2) Moderately, or (3) Well: "))
        except ValueError:
            print("Sorry, I didn't understand that.")
        if (game_variables["food"] - (8 - 5 * input_x)) < game_variables["food"]:
            print("You can't eat that well.")
        elif input_x == 2 and game_variables["ammunition"] < 39:
            print("TOUGH -- You need more bullets to go hunting.")
        else:
            break
    game_variables["food"] = game_variables["food"] - (8 + 5 * input_x)
    game_variables["mileage"] = game_variables["mileage"] + 200 + (
            game_variables["animals"] - 220) / 5 + random.randint(1, 10)
    game_variables["insufficient_clothing"] = False
    game_variables["blizzard"] = False

    return game_variables


def fort(game_variables):
    print("Enter what you wish to spend on the following:")
    # food
    food = buying_routine("food", 0, 9999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - food
    game_variables["food"] = game_variables["food"] + int(.66 * food)

    # ammo
    ammo = buying_routine("ammo", 0, 9999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - ammo
    game_variables["ammunition"] = game_variables["ammunition"] + int(.66 * ammo) * 50

    # clothing
    clothing = buying_routine("clothing", 0, 9999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - clothing
    game_variables["clothing"] = game_variables["clothing"] + int(.66 * ammo) * 50

    # miscellaneous supplies
    misc = buying_routine("clothing", 0, 9999, game_variables["cash"])
    game_variables["cash"] = game_variables["cash"] - misc
    game_variables["supplies"] = game_variables["supplies"] + int(.66 * misc)

    game_variables["mileage"] = game_variables["mileage"] - 45

    return game_variables


def hunting(game_variables):
    # let's check to see if you have enough bullets to go hunting. You need 39 or more.
    if game_variables["ammunition"] > 39:
        my_shooting = shooting()
        game_variables["ammunition"] = game_variables["ammunition"] - (random.randint(1, 10) * 3)

        if my_shooting > 4:
            print("You Missed -- and your dinner got away..")
        elif my_shooting < 3:
            print("Right Between the Eyes - You got a big one!! Full bellies tonight!")
            game_variables["food"] = game_variables["food"] + 52 + (my_shooting * 6)
        else:
            print("Nice Shot! Right on target - Good Eatin' Tonight")
            game_variables["food"] = game_variables["food"] + 48 - (my_shooting * 2)
    else:
        print("You need more bullets to go hunting.")

    game_variables["mileage"] = game_variables["mileage"] - 45
    if game_variables["food"] < 14:
        dying("no_food")

    return game_variables


def do_events(game_variables):
    if random.randint(1, 100) < 50:
        # 33% chance that an event would happen. But, each event would be an incremental sequence
        # of events. If by chance the user has over 16 events, it will be just #16.
        game_variables["event_counter"] = game_variables["event_counter"] + 1
        new_event = game_variables["event_counter"]

        if new_event == 1:
            print("Wagon breaks down - lose time and supplies fixing it")
            game_variables["supplies"] = game_variables["supplies"] - 8
            game_variables["mileage"] = game_variables["mileage"] - random.randint(1, 5)
        elif new_event == 2:
            print("Ox injures leg - slows you down for the rest of trip")
            game_variables["animals"] = game_variables["animals"] - 20
            game_variables["mileage"] = game_variables["mileage"] - 25
        elif new_event == 3:
            print("Bad Luck - Your daughter broke her arm\nYou had to stop and use supplies to make a sling.")
            game_variables["supplies"] = game_variables["supplies"] - 5
            game_variables["mileage"] = game_variables["mileage"] - 5
        elif new_event == 4:
            print("Ox wanders off - spend time looking for it.")
            game_variables["mileage"] = game_variables["mileage"] - 17
        elif new_event == 5:
            print("Your son gets lost - spend half the day looking for him")
            game_variables["mileage"] = game_variables["mileage"] - 10
        elif new_event == 6:
            print("Unsafe water - lose time looking for a clean spring.")
            game_variables["mileage"] = game_variables["mileage"] - random.randint(1, 10) - 2
        elif new_event == 7:
            print("Heavy rains - time and supplies lost")
            game_variables["food"] = game_variables["food"] - 10
            game_variables["ammunition"] = game_variables["ammunition"] - 500
            game_variables["supplies"] = game_variables["supplies"] - 15
            game_variables["mileage"] = game_variables["mileage"] - random.randint(1, 10) - 5
        elif new_event == 8:
            print("Bandits Attack!")
            my_shooting = shooting()
            game_variables["ammunition"] = game_variables["ammunition"] - (my_shooting * 20)
            if game_variables["ammunition"] < 1:
                print("You ran out of bullets - They get lots of cash")
                game_variables["cash"] = int(game_variables["cash"] / 3)
                print("You got shot in the leg and they took one of your oxen.")
                game_variables["injury"] = True
                print("Better have a doc look at your wound.")
                game_variables["supplies"] = game_variables["supplies"] - 5
                game_variables["animals"] = game_variables["animals"] - 20
            else:
                print("Quickest draw outside of Dodge City!!\nYou got 'em!")
        elif new_event == 9:
            print("There was a fire in your wagon - Food and supplies damaged!")
            game_variables["food"] = game_variables["food"] - 40
            game_variables["ammunition"] = game_variables["ammunition"] - 400
            game_variables["mileage"] = game_variables["mileage"] - 15
            game_variables["supplies"] = game_variables["supplies"] - random.randint(1, 8) - 3
        elif new_event == 10:
            print("Lose your way in heavy fog - Time is lost")
            game_variables["mileage"] = game_variables["mileage"] - 10 - random.randint(1, 5)
        elif new_event == 11:
            print("You killed a poisonous snake after it bit you")
            game_variables["ammunition"] = game_variables["ammunition"] - 10
            game_variables["supplies"] = game_variables["supplies"] - 5
            if game_variables["supplies"] < 1:
                print("You die of snakebite since you have no medicine")
                dying("no_supplies")
        elif new_event == 12:
            print("Wagon gets swamped fording river - lose food and clothes.")
            game_variables["food"] = game_variables["food"] - 30
            game_variables["clothing"] = game_variables["clothing"] - 20
            game_variables["mileage"] = game_variables["mileage"] - 20 - random.randint(1, 20)
        elif new_event == 13:
            print("Wild animals attack!")
            if game_variables["ammunition"] < 40:
                print("You were too low on bullets - The wolves overpowered you")
                game_variables["injury"] = True
            else:
                my_shooting = shooting()
                if my_shooting > 2:
                    print("Slow on the draw - They got at your food and clothes.")
                else:
                    print("Nice Shootin' Partner - They didn't get much.")
                game_variables["food"] = game_variables["food"] - (my_shooting * 8)
                game_variables["clothing"] = game_variables["clothing"] - (my_shooting * 4)
                game_variables["ammunition"] = game_variables["ammunition"] - (my_shooting * 20)
        elif new_event == 14:
            print("Cold Weather!!")
            if game_variables["clothing"] > random.randint(1, 4) + 22:
                print("You have enough clothing to keep you warm.")
            else:
                print("You don't have enough clothing to keep you warm.")
                game_variables = illness(game_variables)
        elif new_event == 15:
            print("Hail Storm - Supplies Damaged")
            game_variables["ammunition"] = game_variables["ammunition"] - 200
            game_variables["supplies"] = game_variables["supplies"] - 4 - random.randint(1, 3)
            game_variables["mileage"] = game_variables["mileage"] - 5 - random.randint(1, 10)
        else:
            print("Helpful indians show you where to find more food.")
            game_variables["food"] = game_variables["food"] + 14
    return game_variables


def riders(game_variables):
    my_tactic = 0
    if random.randint(1, 10) > ((game_variables["mileage"] / 100 - 4) ** 2 + 72) / (
            (game_variables["mileage"] / 100 - 4) ** 2 + 12) - 1:
        return
    else:
        if random.randint(1, 10) < 3:
            print("Riders ahead. They don't look hostile.")
            riders_hostile = False
        else:
            print("Riders ahead. They look hostile.")
            riders_hostile = True

        while True:
            try:
                my_tactic = int(builtins.input("\nTactics\n(1) Run (2) Attack (3) Continue (4) Circle Wagons: "))
            except ValueError:
                print("Sorry, I didn't understand that.")
            if my_tactic > 0 or my_tactic < 4:
                break
            else:
                print("Sorry, I didn't understand that.")
        if riders_hostile:
            if my_tactic == 1:
                # Run
                game_variables["mileage"] = game_variables["mileage"] + 20
                game_variables["ammunition"] = game_variables["ammunition"] - 150
                game_variables["animals"] = game_variables["animals"] - 40
            elif my_tactic == 2:
                # attack
                my_shooting = shooting()
                game_variables["ammunition"] = game_variables["ammunition"] - (my_shooting * 40) - 80
                if my_shooting == 1:
                    print("Nice Shooting Tex - You drove them off.")
                elif my_shooting > 4:
                    print("Lousy Shot - You got knifed\nYou have to see Ol' Doc Blanchard.")
                    game_variables["injury"] = True
                else:
                    print("Kinda slow with your Colt .45")
            elif my_tactic == 3:
                # continue
                if random.randint(1, 10) > 7:
                    print("They did not attack.")
                    riders_hostile = False
                else:
                    game_variables["ammunition"] = game_variables["ammunition"] - 150
                    game_variables["mileage"] = game_variables["mileage"] - 15
            else:
                # circle the wagons
                my_shooting = shooting()
                game_variables["ammunition"] = game_variables["ammunition"] - (my_shooting * 30) - 80
                game_variables["mileage"] = game_variables["mileage"] - 25
                if my_shooting == 1:
                    print("Nice Shooting Tex - You drove them off.")
                elif my_shooting > 4:
                    print("Lousy Shot - You got knifed\nYou have to see Ol' Doc Blanchard.")
                    game_variables["injury"] = True
                else:
                    print("Kinda slow with your Colt .45")
        else:
            # riders not hostile.
            if my_tactic == 1:
                # run
                game_variables["mileage"] = game_variables["mileage"] + 15
                game_variables["animals"] = game_variables["animals"] - 10
            elif my_tactic == 2:
                # attack
                game_variables["mileage"] = game_variables["mileage"] - 5
                game_variables["ammunition"] = game_variables["ammunition"] - 100
            elif my_tactic == 3:
                # continue
                game_variables["mileage"] = game_variables["mileage"] - 5
                print("They did not attack.")
            else:
                # circle the wagons.
                game_variables["mileage"] = game_variables["mileage"] - 5
                print("They did not attack.")

    if riders_hostile:
        print("The Riders were hostile - Check for loses.")
        if game_variables["ammunition"] < 1:
            print("You ran out of bullets and got massacred by the riders!")
            dying("injury")
    else:
        print("The Riders were friendly, but check for possible losses.")
    return game_variables


def start_game():
    game_variables = setup()
    if builtins.input("Do you need instructions (yes/no) ") == 'yes':
        instructions()

    game_week_dates = ["March 29", "April 12", "April 26", "May 10", "May 24", "June 7", "June 21", "July 5", "July 19",
                       "August 2", "August 16", "August 31", "September 13", "September 27", "October 11", "October 25",
                       "November 8", "November 22", "December 6", "December 20"]

    print("\nHow good a shot are you with your rifle?")
    print("\t(1) ace marksman,  (2) good shot,  (3) fair to middlin'")
    print("\t(4) need more practice,  (5) shaky knees")
    my_shooting = abs(int(builtins.input(
        "Enter one of the above -- the better you claim you are, the\n"
        "faster you'll have to be with your gun to be successful: ")))
    if my_shooting > 5 or my_shooting < 1:
        my_shooting = 0
    game_variables["shooting_expert_level"] = my_shooting
    game_variables = initial_purchases(game_variables)
    game_variables["game_turn"] = -1

    while True:
        try:
            game_variables["game_turn"] = game_variables["game_turn"] + 1
            if game_variables["game_turn"] < 19:
                if game_variables["mileage"] > 2040:
                    final_turn(game_variables)
                    break
                print("\nMonday, " + game_week_dates[game_variables["game_turn"]] + ", 1847")
                game_loop(game_variables)
                do_events(game_variables)
                riders(game_variables)

                # Check to see if you went far enough. There are no mountains for the first 1000 miles of the journey.
                if game_variables["mileage"] > 950:
                    game_variables = mountains(game_variables)

            else:
                print("\nYou have been on the trail too long\nYour family dies in the first blizzard of winter.")
                dying("")

        except TypeError:
            print(game_variables)
            break


if __name__ == '__main__':
    start_game()
