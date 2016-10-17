#!/usr/bin/python3
# coding=utf-8

# This file contains data on the screens in the game

import time
import items

import ascii_helper
import figlet_helper
import screen
from debug import dprint
from misc_utils import *

screen_stack = []

previous_screen = None
current_screen = None


def open_screen(new_screen):
    global previous_screen
    global current_screen

    was_same_screen = new_screen is current_screen

    previous_screen = current_screen
    current_screen = new_screen

    previous_screen_name = "console"

    if previous_screen is not None:
        previous_screen_name = previous_screen["name"]

    if not was_same_screen and not new_screen["one_time"]:
        screen_stack.append(new_screen)
        dprint("Moving from the " + previous_screen_name + " screen to the " + current_screen["name"] + " screen.")
        dprint("Stack size: " + str(len(screen_stack)))

    new_screen["draw_function"]()

    if not was_same_screen and not new_screen["one_time"] and previous_screen is not None:
        if len(screen_stack) > 1:
            previous_screen = screen_stack.pop()
            current_screen = screen_stack.pop()
            screen_stack.append(current_screen)
            dprint("Moving from the " + previous_screen["name"] + " screen to the " + current_screen["name"] + " screen.")
            dprint("Stack size: " + str(len(screen_stack)))
        elif len(screen_stack) > 0:
            current_screen = screen_stack.pop()
            screen_stack.append(current_screen)

            previous_screen_name = "console"

            if previous_screen is not None:
                previous_screen_name = previous_screen["name"]

            dprint("Moving from the " + previous_screen_name + " screen to the " + current_screen["name"] + " screen.")
            dprint("Stack size: " + str(len(screen_stack)))


def draw_starting_screen():
    # TODO: This function should not return until they have picked all 4 characters' names
    # TODO: These names should be updated in the survivors list in survivors.py, where survivors[0] is the main player

    # TODO: use the input function to ask for the players name, and for three other friends they can count on eg: input("What is your name? ")

    # TODO: update the names in survivors.py by using the survivors list eg: survivors[0] = player_name

    # TODO: enforce names so that they are not longer than 16 characters

    # TODO: the player should be informed about what they start with, how much food, how many medkits, how much money

    title_text = "Survival Trail"

    big_font = figlet_helper.load_font("resources/fonts/big.flf")

    title_width = figlet_helper.get_text_width(title_text, big_font)

    start_title_x = int((screen.get_width() / 2) - (title_width / 2))

    while True:
        screen.clear()
        screen.draw_ascii_font_text(start_title_x, 0, title_text, big_font)

        screen.draw_text(45, 11, "1. Travel to the trail")
        screen.draw_text(45, 13, "2. Learn about the trail")
        screen.draw_text(45, 15, "3. Exit the trail")
        screen.draw_text(42, 17, "Enter your option: ")
        screen.set_cursor_position(42 + 19, 17)
        screen.flush()

        user_input = input()

        if user_input == "1":
            open_screen(screen_list["survivor_name"])

            return
        elif user_input == "2":
            open_screen(screen_list["info"])
        elif user_input == "3":
            screen.clear()
            quit()
        else:
            continue

        return


def draw_info_screen():
    pass


def get_max_user_input(print_text, alt_text, max_length):
    user_input = input(print_text)

    while len(user_input) > max_length:
        user_input = input(alt_text)
    return user_input


def draw_survivor_name_screen():
    screen.clear()
    name = get_max_user_input("Enter your name: ", "Enter a valid name: ", 16)
    # Leave the name as default when player enters nothing
    if len(name) > 0:
        survivors.survivor_list[0]["name"] = name

    for i in range(0, 3):
        name = get_max_user_input("Enter your friend's name: ", "Enter a valid friend's name: ", 16)
        if len(name) > 0:
            survivors.survivor_list[i + 1]["name"] = name

    open_screen(screen_list["city"])


def draw_dead_screen():
    screen.clear()

    game_over_image = ascii_helper.load_image("resources/dead_game_over.ascii")
    tombstone_image = ascii_helper.load_image("resources/dead_tombstone.ascii")

    game_over_x = int((screen.get_width() / 2) - (game_over_image["width"] / 2)) - 1
    tombstone_x = int((screen.get_width() / 2) - (tombstone_image["width"] / 2))

    screen.draw_ascii_image(game_over_x, 0, game_over_image)
    screen.draw_ascii_image(tombstone_x, game_over_image["height"] + 2, tombstone_image)

    screen.flush()

    time.sleep(2)

    screen.print_notification("Press any key to continue.", False)

    open_screen(screen_list["points"])


def draw_win_screen():
    screen.clear()

    big_font = figlet_helper.load_font("resources/fonts/big.flf")
    contessa_font = figlet_helper.load_font("resources/fonts/contessa.flf")

    win_title_text = "You Win!"
    win_body_text = "You reached New York in time"

    win_title_width = figlet_helper.get_text_width(win_title_text, big_font)
    win_body_width = figlet_helper.get_text_width(win_body_text, contessa_font)

    win_title_x = int((screen.get_width() / 2) - (win_title_width / 2))
    win_body_x = int((screen.get_width() / 2) - (win_body_width / 2))

    screen.draw_ascii_font_text(win_title_x, 0, win_title_text, big_font)
    screen.draw_ascii_font_text(win_body_x, big_font["height"], win_body_text, contessa_font)

    screen.flush()

    time.sleep(6)

    screen.print_notification("Press any key to continue.", False)

    open_screen(screen_list["points"])


# TODO: this needs some prettifying
def draw_points_screen():
    screen.clear()

    points = 0

    points += survivors.distance_travelled

    points += count_survivors(True, False, False, False) * 250

    score_title_image = ascii_helper.load_image("resources/numbers/score_title.ascii")
    score_title_x = int((screen.get_width() / 2) - (score_title_image["width"] / 2))

    screen.draw_ascii_image(score_title_x, 0, score_title_image)
    screen.draw_ascii_numbers(0, score_title_image["height"] + 5, int(points))

    screen.flush()

    time.sleep(2)

    screen.print_notification("Press any key to exit.", False)

    screen.clear()

    quit()


def draw_city_screen():
    # TODO: think of some way to reliably get the city here
    city = cities.city_list["Los Angeles"]

    while True:
        screen.clear()
        print("You enter the city of " + city["name"])

        # Show options to player:
        print("You can:")
        print("1: Get information on " + city["name"] + ".")
        print("2: Check survivors status.")
        print("3: Trade with other survivors.")
        print("4: Go to the bar.")
        print("5: Rest.")
        print("6: Move on to " + get_next_city(survivors.distance_travelled + survivors.car_speed)["name"] + ".")
        print("")
        player_choice = input("What would you like to do? ")

        # Evaluate the players decision:
        player_choice = normalise_input(player_choice)
        if player_choice == "1":
            screen.clear()
            # Get information
            print("You are in " + city["name"] + ".")
            print(city["description"])
            # TODO: Maybe information on whats available, like traders, inns to stay, etc...?
            print("The next city is " + get_next_city(survivors.distance_travelled + survivors.car_speed)["name"] + ".")

            # Return to options
            input("Press enter to go back...")
        elif player_choice == "2":
            # Check status
            open_screen(screen_list["put_down"])
        elif player_choice == "3":
            # Trade
            open_screen(screen_list["trading"])
        elif player_choice == "4":
            # Bar
            pass
        elif player_choice == "5":
            # Rest
            open_screen(screen_list["resting"])
        elif player_choice == "6":
            # Continue to previous screen
            return
        # TODO: Remove after debugged
        elif player_choice == "7":
            # Debugging for dead screen
            open_screen(screen_list["dead"])
        # TODO: Remove after debugged
        elif player_choice == "8":
            # Debugging for dead screen
            open_screen(screen_list["points"])
        elif player_choice == "9":
            # Debugging for win screen
            open_screen(screen_list["win"])
        # TODO: Remove after debugged
        else:
            # Invalid input
            print("Please enter a number between 1 and 6.")


def draw_trading_screen():
    screen.clear()

    city = get_next_city(survivors.distance_travelled)

    trades = []

    if "saved_trades" in city:
        trades = city["saved_trades"]
    else:
        previous_trades = []

        for i in range(5):
            # None means use money
            survivors_item = None

            random_survivors_item_unit_value = 1

            # 60% chance, use random item - otherwise use money for this trade
            if random.randrange(1, 100) <= 60:
                # Get a random item from the group inventory
                survivors_item = get_random_dict_value(items.item_list)

            if survivors_item is not None:
                random_survivors_item_unit_value = random.randrange(survivors_item["min_value"], survivors_item["max_value"])

            for j in range(10):
                # TODO: let the trader offer money for items if the survivor item is not money
                trader_item = None

                if survivors_item is None or random.randrange(1, 100) <= 60:
                    trader_item = get_random_dict_value(items.item_list)

                for previous_trade in previous_trades:
                    if previous_trade[0] == survivors_item and previous_trade[1] == trader_item:
                        break

                random_trader_item_unit_value = 1

                if trader_item is not None:
                    random_trader_item_unit_value = random.randrange(trader_item["min_value"], trader_item["max_value"])

                # TODO: what if this doesn't convert to int exactly?
                survivors_item_amount = random_trader_item_unit_value / random_survivors_item_unit_value

                if survivors_item_amount < 1:
                    survivors_item_amount = 1

                trader_item_amount = random_survivors_item_unit_value / random_trader_item_unit_value

                if trader_item_amount < 1:
                    trader_item_amount = 1

                if survivors_item is None or trader_item != survivors_item:
                    if random_survivors_item_unit_value <= 10 and survivors_item_amount <= 10:
                        random_increase = random.randrange(11 - random_survivors_item_unit_value, 15 - random_survivors_item_unit_value)

                        survivors_item_amount *= random_increase
                        trader_item_amount *= random_increase

                    previous_trades.append([survivors_item, trader_item])

                    trades.append({"survivors_item": survivors_item, "trader_item": trader_item,
                                   "survivors_item_amount": survivors_item_amount, "trader_item_amount": trader_item_amount})

                    break

    city["saved_trades"] = trades

    for trade in trades:
        survivors_item = trade["survivors_item"]
        trader_item = trade["trader_item"]
        survivors_item_amount = trade["survivors_item_amount"]
        trader_item_amount = trade["trader_item_amount"]

        survivors_item_name = "Money"

        if survivors_item is not None:
            survivors_item_name = survivors_item["plural_name"]

        trader_item_name = "Money"

        if trader_item is not None:
            trader_item_name = trader_item["plural_name"]

        print("1: Continue to next trade")
        print("2: Trade " + str(int(survivors_item_amount)) + " of your " + survivors_item_name + " for " + str(
            int(trader_item_amount)) + " of their " + trader_item_name)
        print("3: Skip all further trades")
        print("")

        while True:
            user_input = input("What would you like to do? ")

            if user_input == "1":
                screen.clear()
                break
            elif user_input == "2":
                if survivors_item is None:
                    if survivors.group_money >= survivors_item_amount:
                        survivors.group_money -= survivors_item_amount
                        screen.print_notification("Trade completed successfully.", False)

                        if trader_item is None:
                            survivors.group_money += trader_item_amount
                        else:
                            survivors.inventory_add_item(trader_item, trader_item_amount)

                        city["saved_trades"].remove(trade)
                    else:
                        screen.print_notification(
                            "Trade failed, you do not have enough " + survivors_item_name + " for this trade.", False)
                else:
                    if survivors.inventory_remove_item(survivors_item, survivors_item_amount):
                        screen.print_notification("Trade completed successfully.", False)

                        if trader_item is None:
                            survivors.group_money += trader_item_amount
                        else:
                            survivors.inventory_add_item(trader_item, trader_item_amount)

                        city["saved_trades"].remove(trade)
                    else:
                        screen.print_notification(
                            "Trade failed, you do not have enough " + survivors_item_name + " for this trade.", False)

                screen.clear()

                break
            if user_input == "3":
                screen.print_notification("Skipped all further trades.", False)
                return
            else:
                continue

    screen.print_notification("There are no more trades to show.", False)


def draw_resting_screen():
    screen.clear()

    print("This is the resting screen")
       
    for i in range(0, len(survivors.survivor_list)):
        if survivors.survivor_list[i]["health"] == survivors.survivor_list[i]["max_health"]:
            print(survivors.survivor_list[i]["name"] + ":" + "You don't need to rest")
    # Show options to player:
        elif survivors.survivor_list[i]["health"] <= survivors.survivor_list[i]["max_health"]: 
            print(survivors.survivor_list[i]["name"] + ":") 
            print("1: one hour = 10 health")
            print("2: two hours = 20 health")
            print("3: three hours = 30 health")
            print("4: four hours = 40 health")
            print("5: five hours = 50 health")
            print("6: six hours = 60 health")
            print("7: seven hours = 70 health")
            print("8: eight hours = 80 health")
            print("9: nine hours = 90 health")
            print("")        
            sleep_choice = input("How many hours would you like to sleep? ")
            sleep_choice = normalise_input(sleep_choice)

            if sleep_choice == "1":
                print(int(survivors.survivor_list[i]["health"]) + 10)
            elif sleep_choice == "2":
                print(int(survivors.survivor_list[i]["health"]) + 20)
            elif sleep_choice == "3":
                print(int(survivors.survivor_list[i]["health"]) + 30)
            elif sleep_choice == "4":
                print(int(survivors.survivor_list[i]["health"]) + 40)
            elif sleep_choice == "5":
                print(int(survivors.survivor_list[i]["health"]) + 50)
            elif sleep_choice == "6":
                print(int(survivors.survivor_list[i]["health"]) + 60)
            elif sleep_choice == "7":
                print(int(survivors.survivor_list[i]["health"]) + 70)
            elif sleep_choice == "8":
                print(int(survivors.survivor_list[i]["health"]) + 80)
            elif sleep_choice == "9":
                print(int(survivors.survivor_list[i]["health"]) + 90)
            else:
                print("Please enter a number between 1 and 9.")

    screen.wait_key()


def draw_put_down_screen():
    screen.clear()
    # Display the survivors status

    # Players information:
    if not survivors.survivor_list[0]["bitten"]:
        print("Your health is " + str(survivors.survivor_list[0]["health"]) + ".")
    else:
        print("Your health is " + str(survivors.survivor_list[0]["health"]) + ", and you have been bitten.")

    # Other survivors information:
    for survivor in survivors.survivor_list:
        if survivor["alive"] and not survivor["bitten"]:
            print(survivor["name"] + " has " + str(survivor["health"]) + " health.")
        elif survivor["alive"] and survivor["bitten"] and not survivor["zombified"]:
            print(survivor["name"] + " has " + str(survivor["health"]) + " health, and has been bitten")
        elif not survivor["alive"]:
            print(survivor["name"] + " is dead.")

    print("")

    # Display options
    while True:
        option_count = 2
        options_available = {}

        print("1: Go back")
        print("2: Commit suicide")

        for i in range(1, len(survivors.survivor_list)):
            if survivors.survivor_list[i]["alive"]:
                option_count += 1
                options_available.update({option_count: i})
                print(str(option_count) + ": Put down " + str(survivors.survivor_list[i]["name"]) + ".")

        # Evaluate users input:
        user_choice = input("What would you like to do? ")

        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a number.")
            continue

        if user_choice == 1:
            # Return to city menu screen
            return
        elif user_choice == 2:
            # Suicide
            open_screen(screen_list["dead"])
        elif user_choice <= option_count:
            # Search through options available to find who to kill
            survivors.survivor_list[options_available[user_choice]]["alive"] = False
            print("You killed " + survivors.survivor_list[options_available[user_choice]]["name"])
            continue
        else:
            print("Please enter a number between 1 and " + str(option_count) + ".")
            continue

        return


def draw_travelling_screen():
    if previous_screen is None:
        open_screen(screen_list["starting"])

    show_next_city_notification = previous_screen is not None and previous_screen["name"] == "city"

    car_body_image = ascii_helper.load_image("resources/car_body.ascii")
    car_wheel_image_1 = ascii_helper.load_image("resources/car_wheel_1.ascii")
    car_wheel_image_2 = ascii_helper.load_image("resources/car_wheel_2.ascii")

    survivor_x_start = int(screen.get_width() / 10)
    survivor_y_start = screen.get_height() - (len(survivors.survivor_list) * 2) - 1

    car_x = int((screen.get_width() / 2) - (car_body_image["width"] / 2))
    car_y = survivor_y_start - car_body_image["height"] - 5

    # TODO: This is kinda messy
    iterations = 0
    wheel = 0
    road = 0

    while True:
        # Draw travelling progress bar
        progress_bar_box_width = int(screen.get_width() / 1.5)
        progress_bar_box_x = int((screen.get_width() / 2) - (progress_bar_box_width / 2))

        progress_bar_width = progress_bar_box_width - 6

        screen.draw_bordered_rect(progress_bar_box_x, -1, progress_bar_box_width, 5)

        screen.draw_pixel(int(progress_bar_box_x + 2), 1, "|")
        screen.draw_pixel(int(progress_bar_box_x + progress_bar_width + 3), 1, "|")

        for x in range(progress_bar_box_x + 3, progress_bar_box_x + progress_bar_box_width - 3):
            screen.draw_pixel(x, 1, "-")

        progress_bar_current_x = progress_bar_box_x + 3 + (
            (survivors.distance_travelled / get_end_distance()) * progress_bar_width)

        screen.draw_pixel(int(progress_bar_current_x), 2, "^")

        # Draw survivors stats
        survivor_y = survivor_y_start

        health_x = 0

        for survivor in survivors.survivor_list:
            survivor_name = survivor["name"]
            survivor_name_length = len(survivor_name)

            if survivor_name_length > health_x:
                health_x = survivor_name_length

            screen.draw_text(survivor_x_start, survivor_y + 1, survivor_name)

            survivor_y += 2

        survivor_y = survivor_y_start + 1

        total_bars = 14

        for survivor in survivors.survivor_list:
            if survivor["alive"]:
                screen.draw_progress_bar(survivor_x_start + health_x + 2, survivor_y, total_bars,
                                         survivor["health"] / survivor["max_health"])

                if survivor["zombified"]:
                    screen.draw_text(survivor_x_start + health_x + total_bars + 5, survivor_y, "(ZOMBIE)")
                elif survivor["bitten"]:
                    screen.draw_text(survivor_x_start + health_x + total_bars + 5, survivor_y, "(BITTEN)")
            else:
                padding = int((total_bars - 4) / 2)
                screen.draw_text(survivor_x_start + health_x + 2, survivor_y,
                                 "[" + (padding * " ") + "DEAD" + (padding * " ") + "]")

            survivor_y += 2

        # Draw stats
        next_city = get_next_city(survivors.distance_travelled)

        stat_lines = ["Time: " + format_time(survivors.current_datetime),
                      "Date: " + format_date(survivors.current_datetime),
                      "Next City: " + next_city["name"], "Distance: " + str(
                int(next_city["distance_from_start"] - survivors.distance_travelled)) + " miles"]

        longest_line = 0

        for stat_line in stat_lines:
            stat_line_length = len(stat_line)
            if stat_line_length > longest_line:
                longest_line = stat_line_length

        stat_x = int(screen.get_width() - longest_line - (screen.get_width() / 10) + 2)
        stat_y = survivor_y_start + 1

        for stat_line in stat_lines:
            screen.draw_text(stat_x, stat_y, stat_line)

            stat_y += 2

        # Draw the car
        screen.draw_ascii_image(car_x, car_y, car_body_image)

        if wheel <= 0.25:
            screen.draw_ascii_image(car_x + 14, car_y + 7, car_wheel_image_2)
            screen.draw_ascii_image(car_x + 53, car_y + 7, car_wheel_image_2)
        else:
            screen.draw_ascii_image(car_x + 14, car_y + 7, car_wheel_image_1)
            screen.draw_ascii_image(car_x + 53, car_y + 7, car_wheel_image_1)

        for x in range(screen.get_width()):
            pixel_char = "="

            if road < 1:
                if x % 2 == 0:
                    pixel_char = "-"
            else:
                if x % 2 != 0:
                    pixel_char = "-"

            screen.draw_pixel(x, car_y + car_body_image["height"] + 2, pixel_char)

        screen.flush()

        if show_next_city_notification:
            next_city = get_next_city(survivors.distance_travelled)
            screen.print_notification(next_city["name"] + " is " + str(
                int(next_city["distance_from_start"] - survivors.distance_travelled)) + " miles away.")
            show_next_city_notification = False

        wheel += 0.25
        road += 1

        if wheel > 1:
            iterations += 1

            if iterations > 2:
                return

        if road > 1:
            road = 0

        time.sleep(0.15)


screen_list = {
    "starting": {
        "name": "starting",

        "draw_function": draw_starting_screen,

        "one_time": True
    },

    "dead": {
        "name": "dead",

        "draw_function": draw_dead_screen,

        "one_time": True
    },

    "win": {
        "name": "win",

        "draw_function": draw_win_screen,

        "one_time": True
    },

    "points": {
        "name": "points",

        "draw_function": draw_points_screen,

        "one_time": True
    },

    "city": {
        "name": "city",

        "draw_function": draw_city_screen,

        "one_time": False
    },

    "trading": {
        "name": "trading",

        "draw_function": draw_trading_screen,

        "one_time": False
    },

    "resting": {
        "name": "resting",

        "draw_function": draw_resting_screen,

        "one_time": False
    },

    "put_down": {
        "name": "put_down",

        "draw_function": draw_put_down_screen,

        "one_time": False
    },

    "travelling": {
        "name": "travelling",

        "draw_function": draw_travelling_screen,

        "one_time": False
    },

    "info": {
        "name": "info",

        "draw_function": draw_info_screen,

        "one_time": False
    },

    "survivor_name": {
        "name": "survivor_name",

        "draw_function": draw_survivor_name_screen,

        "one_time": True
    },
}
