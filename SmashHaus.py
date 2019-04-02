##########################################################################
#                                                                        #
# Program title :                                                        #
#   SmashHaus.py                                                         #
#                                                                        #
# Brief Overview :                                                       #
#     A program designed to create and manage the infrastructure for a   #
#   small scale Smash Bros leaderboard. This includes a leaderboard,     #
#   an elo rating system, a match history, and a stat tracker for        #
#   each player.                                                         #
#                                                                        #
# Written by :                                                           #
#   Nick O'Brien                                                         #
#                                                                        #
# Version 1.0                                                            #
#                                                                        #
# Date Published :                                                       #
#   April 01, 2019                                                       #
#                                                                        #
##########################################################################

import csv
import math

def current_standings(info):

    name_rank = []

    if info['players'] == 0:
        print("There are no registered users.")
        return

    for names in info.items():
        temp = []
        
        if names[0] == 'players':
            continue
        else:
            temp.append(names[0])
            temp.append(int(names[1][1]))
        name_rank.append(temp)

    for i in range(len(name_rank)):
        name_rank[i].reverse()    
    name_rank = sorted(name_rank)
    name_rank.reverse()
    

    current = name_rank[0][0]
    count = 2
    print("\nCurrent standings")
    print("=================")
    print("1) " + str(name_rank[0][1]) + " : " + str(name_rank[0][0]))
    for i in range(1,len(name_rank)):
        if name_rank[i][0] == current:
            print("   " + str(name_rank[i][1]) + " : " + str(name_rank[i][0]))
        else:
            print(str(count) + ") "+ str(name_rank[i][1]) + " : "  + str(name_rank[i][0]))
            count += 1
            current = name_rank[i][0]
    print()

    return


def match_results(info,usernames_lower_case,usernames):
    
    if info['players'] == 0:
        print("There are no registered users.")
        return

    history = open("match_history.csv", "a")
    
    print("\nHere is a list of players.")
    count = 0
    for name in info.items():
        if name[0] == 'players':
            continue
        elif count == 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        elif count % 2 != 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        else:
            print(str(count + 1) + ")", end = " ")
            print(name[0])
            count += 1  

    if count % 3 != 0:
        print("\n\nEnter the usernames of the players that played.")
    else:
        print("\nEnter the usernames of the players that played.")

    # TODO : Cut down on search time by using binary search to find username.

    player1 = input("Player 1 :: ")
    while player1.lower() not in usernames_lower_case:
        print("Player not found. Try again.")
        player1 = input("Player 1 :: ")

    player2 = input("Player 2 :: ")
    while player2.lower() not in usernames_lower_case:
        print("Player not found. Try again.")
        player2 = input("Player 2 :: ")

    players = [player1.lower(),player2.lower()]

    print("\nWho won the match?", usernames[usernames_lower_case.index(player1.lower())],"or", usernames[usernames_lower_case.index(player2.lower())] + "?")
    result = input(" :: ")
    while result.lower() not in players:
        print("Please enter a valid response.")
        result = input(" :: ")

    player1 = usernames[usernames_lower_case.index(player1.lower())]
    player2 = usernames[usernames_lower_case.index(player2.lower())]

    print("\nWhat was the score? Enter the number associated with the score.")
    print("1) 2-0\n2) 2-1")
    score = input(" :: ")
    while score < '1' or score > '2':
        print("Please enter a valid response.")
        score = input(" :: ")    
    
    if result == '1':
        result = player1
    else:
        result = player2

    if score == '1':
        score = "2-0"
    else:
        score = "2-1"

    # Add results to match history

    history.write(str(player1) + ',' + str(player2) + ',' + str(result) + ',' + str(score) + "\n")
    history.close()

    # Run algorithm for updating the player ratings.

    player1_rating = int(info[player1][1])
    player2_rating = int(info[player2][1])


    prob_player1_wins = (1.0/(1.0+math.pow(10,((player2_rating - player1_rating)/400))))
    prob_player2_wins = (1.0/(1.0+math.pow(10,((player1_rating - player2_rating)/400))))

    prob_player1_wins = round(prob_player1_wins,2)
    prob_player2_wins = round(prob_player2_wins,2)

    k = 50

    expected_winner = ""

    if prob_player1_wins > prob_player2_wins:
        expected_winner = player1
    else:
        expected_winner = player2

    if player1 == expected_winner:
        if expected_winner == result:
            player1_rating = int(player1_rating + k*(1-prob_player1_wins))
            player2_rating = int(player2_rating + k*(0-prob_player2_wins))
        else:
            player1_rating = int(player1_rating + k*(0-prob_player1_wins))
            player2_rating = int(player2_rating + k*(1-prob_player2_wins))
    else:
        if expected_winner == result:
            player1_rating = int(player1_rating + k*(0-prob_player1_wins))
            player2_rating = int(player2_rating + k*(1-prob_player2_wins))
        else:
            player1_rating = int(player1_rating + k*(1-prob_player1_wins))
            player2_rating = int(player2_rating + k*(0-prob_player2_wins))

    print("\n" + player1 + "'s new rating :", player1_rating)
    print(player2 + "'s new rating :", player2_rating)

    # Update ratings in the dictionary
    
    info[player1][1] = str(player1_rating)
    info[player2][1] = str(player2_rating)
    
    # Update 'Games' column in the dictionary

    info[player1][2] = str(int(info[player1][2]) + 1)
    info[player2][2] = str(int(info[player2][2]) + 1)
    
    # Update 'Wins' column in the dictionary

    if result == player1:
        info[player1][3] = str(int(info[player1][3]) + 1)
        info[player2][4] = str(int(info[player2][4]) + 1)
    else:
        info[player2][3] = str(int(info[player2][3]) + 1)
        info[player1][4] = str(int(info[player1][4]) + 1)


    x = usernames.index(player1)
    y = usernames.index(player2)
    info_player1 = player1 + ','
    info_player2 = player2 + ','
    

    file1 = open("information.csv", "r")
    update_players = file1.readlines()


    for i in range(len(info[player1])):
        if i == len(info[player1]) - 1:
            info_player1 += info[player1][i] + '\n'
        else:
            info_player1 += info[player1][i] + ','
    for i in range(len(info[player2])):
        if i == len(info[player2]) - 1:
            info_player2 += info[player2][i] + '\n'
        else:
            info_player2 += info[player2][i] + ','

    update_players[x+1] = info_player1
    update_players[y+1] = info_player2
    
    file1.close()
    file1 = open("information.csv", "w")
    file1.writelines(update_players)
    file1.close()

    return


def get_match_history(info, usernames_lower_case, usernames):
    
    if info['players'] == 0:
        print("There are no registered users.")
        return

    history = open("match_history.csv" , "r")
    history_dict = {}
    game = 0

    history = history.readlines()
    for i in range(len(history)):
        history[i] = history[i].strip()
        history[i] = history[i].split(",")
        history_dict[game] = history[i]
        game += 1
    
    print("\nHere is a list of players.")
    count = 0
    for name in info.items():
        if name[0] == 'players':
            continue
        elif count == 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        elif count % 2 != 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        else:
            print(str(count + 1) + ")", end = " ")
            print(name[0])
            count += 1  

    if count % 3 != 0:
        print("\n\nWho's match history would you like to view? Enter their username.")
    else:
        print("\nWho's match history would you like to view? Enter their username.")

    user_history = input(" :: ")
    while user_history.lower() not in usernames_lower_case:
        print("Please enter a valid username")
        user_history = input(" :: ")

    user_history = usernames[usernames_lower_case.index(user_history.lower())]

    print("\n" + user_history + "'s match history. \n")
    print(format("   Players", "<33"), end = "")
    print(format("Winner", "<15"), end = "")
    print("Score\n=======================================================")

    names_printed = 0

    for names in history_dict.items():
        
        if names[0] == 0:
            continue
        elif names[1][0] == user_history or names[1][1] == user_history:
            print(str(names_printed + 1) + ") ", end = "")
            print(format(names[1][0], "<15"), end = "")
            print(format(names[1][1], "<15"), end = "")
            print(format(names[1][2], "<15"), end = "")
            print(names[1][3])
            names_printed += 1
        else:
            continue
    
    if names_printed == 0:
        print("Player has no matches on record.")



    return


def add_player(info, usernames_lower_case):

    rating = '1200'
    games = '0'

    outf = open("information.csv", "a")
    check = False
    confirm = ''


    while not check:
        username = input("\nEnter your username. \n :: ")
        #Check length
        if len(username) > 12:
            print("\nUsername can't exceed 12 characters.")
            continue
        #Check repeats
        if username.lower() in usernames_lower_case:
            print("\nUsername already taken. Enter a different username.")
            continue
        #Check user validation
        valid = ['y','n']
        confirm = input("\nIs [" + username + "] the username you want? Yes(y) | No(n). \n :: ")

        while confirm.lower() not in valid:
            print("\nEnter a valid response.")
            confirm = input("Is [" + username + "] the username you want? Yes(y) | No(n). \n :: ") 
            
        if confirm.lower() == 'n':
            continue
        #If user confirms, exit loop. Move on.
        if confirm.lower() == 'y':
            check = True


    #Do same method for user's name.
    check = False
    while not check:
        name = input("\nEnter your first name and the first initial of your last name. \n :: ")

        valid = ['y','n']
        confirm = input("\nIs [" + name + "] the correct name? Yes(y) | No(n). \n :: ")

        while confirm.lower() not in valid:
            print("\nEnter a valid response.")
            confirm = input("Is [" + name + "] the correct name? Yes(y) | No(n). \n :: ") 
            
        if confirm.lower() == 'n':
            continue
        if confirm.lower() == 'y':
            check = True


    profile = username + ',' + name + ',' + rating + ',' + games + ',' + games + ',' + games

    outf.write(profile + '\n')
    outf.close()

    info[username] = [name,rating,games,games,games]
    info['players'] += 1

    file1 = open("information.csv", "r")
    update_players = file1.readlines()
    update_players[1] = (str(info['players']) +",,,,,\n")
    file1.close()
    file1 = open("information.csv", "w")
    file1.writelines(update_players)
    file1.close()

    print("\nDone")

    return info


def remove_player(info, usernames):

    if info['players'] == 0:
        print("There are no registered users.")
        return

    password = "FuckSahil"

    print("\nHere is a list of players.")
    count = 0
    for name in info.items():
        if name[0] == 'players':
            continue
        elif count == 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        elif count % 2 != 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        else:
            print(str(count + 1) + ")", end = " ")
            print(name[0])
            count += 1  

    if count % 3 != 0:
        print("\n\nPlease enter the username of the player you would like to remove.")
        print("This area is case sensitive.")
    
    else:
        
        print("\nPlease enter the username of the player you would like to remove.")
        print("This area is case sensitive.")
    

    remove_user = input(" :: ")
    while remove_user not in usernames:
        print("Please enter a valid username.")
        remove_user = input(" :: ")
    
    print("\nThis process requires admin approval.")
    input_password = input("Password :: ")
    while input_password != password:
        print("Invalid password.")
        input_password = input("Password :: ")

    file2 = open("information.csv", "r")
    file_remove = file2.readlines()
    counter = 1
    for names in info.items():
    
        if names[0] == remove_user:
            break
        else:
            counter += 1
    file_remove.pop(counter)
    file2.close()
    file2 = open("information.csv", "w")
    file2.writelines(file_remove)
    file2.close()

    info['players'] -= 1

    file1 = open("information.csv", "r")
    update_players = file1.readlines()
    update_players[1] = (str(info['players']) +",,,,,\n")
    file1.close()
    file1 = open("information.csv", "w")
    file1.writelines(update_players)
    file1.close()

    print('Done')

    info.pop(remove_user)

    return info


def get_player_stats(info,usernames_lower_case,usernames):

    if info['players'] == 0:
        print("There are no registered users.")
        return
    
    print("\nHere is a list of players.")
    count = 0
    for name in info.items():
        if name[0] == 'players':
            continue
        elif count == 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        elif count % 2 != 0:
            print(str(count + 1) + ")", end = " ")
            print(format(name[0], "<15"), end = "")
            count += 1
        else:
            print(str(count + 1) + ")", end = " ")
            print(name[0])
            count += 1  

    if count % 3 != 0:
        print("\n\nPlease enter a player's username.")
    
    else:
        print("\nPlease enter a player's username.")
        
    user_stats = input(" :: ")
    while user_stats.lower() not in usernames_lower_case:
        print("Please enter a valid username.")
        user_stats = input(" :: ")

    user_stats = usernames[usernames_lower_case.index(user_stats.lower())]
    name = info[user_stats][0]
    rating = info[user_stats][1]
    games_played = info[user_stats][2]
    wins = info[user_stats][3]
    losses = info[user_stats][4]
    if wins != '0' and losses != '0':
        winrate = (str(((round(int(wins)/int(games_played),4)))*100)) + "%"
    elif wins != '0' and losses == '0':
        winrate = wins
    elif wins == '0' and losses != '0':
        winrate = '0'
    else:
        winrate = '0'

    more_equals = len(user_stats) - 4
    
    

    print('\n' + user_stats + "'s Statistics")
    print("=================", end = "")
    if more_equals > 0:
        for i in range(more_equals):
            print("=", end = "")
    print("\nName : " + name)
    print("Rating : " + rating)
    print(" played : " + games_played)
    print("Wins : " + wins)
    print("Losses : " + losses)
    print("Winrate : " + winrate)

    return


def rating_override(info,usernames_lower_case,usernames):

    print("\nShhhhhhhh it's a secret.")
    print("\nEnter the username of the player whose rating you'd like to override.")
    name_override = input(" :: ")
    while name_override.lower() not in usernames_lower_case:
        print("Enter a valid username")
        name_override = input(" :: ")

    name_override = usernames[usernames_lower_case.index(name_override.lower())]

    print("\nWhat should their new rating be?")
    rank_override = input(" :: ")
    while rank_override < '0' or rank_override > '9999':
        print("\nOverride rating must be between 0 and 9999.")
        rank_override = input(' :: ')

    info[name_override][1] = rank_override

    file1 = open("information.csv", "r")
    update_player = file1.readlines()
    x = usernames.index(name_override)
    y = update_player[x+1].split(',')
    y[2] = rank_override
    z = ''
    a = y[:]
    for i in range(len(y)):
        if i == len(y) - 1:
            z += a.pop(0)
        else:
            z += a.pop(0) + ','

    update_player[x+1] = z
    file1.close()
    file1 = open("information.csv", "w")
    file1.writelines(update_player)
    file1.close()

    print('Done')


    return info


def main():

    inf = open("information.csv", "r")

    x = inf.readline()

    num_players = inf.readline().strip()
    num_players = int(num_players[0])

    #print(num_players)

    info = {}
    info["players"] = num_players

    # Username, Name, Elo, Games, Wins, Losses

    for i in range(num_players):
        
        x = inf.readline().strip()

        # turn into list

        x = x.split(",")

        y = x.pop(0)

        info[y] = x

    inf.close()

    usernames_lower_case = []

    for name in info.items():
        usernames_lower_case.append(name[0].lower())

    if info['players'] == 0:
        print("\n# ============================================================ #")
        print("There are no registered users. Start by adding two new players.")
        print("# ============================================================ #")
        for i in range(1,3):
            print("\nPlayer " + str(i) + " :")
            info = add_player(info,usernames_lower_case)
            usernames_lower_case = []

            for name in info.items():
                usernames_lower_case.append(name[0].lower())

    
    if info['players'] == 1:
        print("\n# ============================================================ #")
        print("There is only one registered user. Add one more player.")
        print("# ============================================================ #")
        for i in range(1):
            print("\nPlayer " + str(2) + " :")
            info = add_player(info,usernames_lower_case)


    a = "Smash Hoüs 405"
    b = "What would you like to do?"
    c = "Enter the number of the task you would like to run."
    a = a.center(60)
    b = b.center(60)
    c = c.center(60)

    print("# ============================================================== #")
    print("|| " + a + " ||")
    print("|| " + b + " ||")
    print("|| " + c + " ||")
    print("|| " + format(" ||", ">63"))
    print("|| 1. Current standings" + format(" ||", ">43"))
    print("|| 2. Report match results." + format(" ||", ">39"))
    print("|| 3. Get player match history." + format(" ||", ">35"))
    print("|| 4. Get player statistics." + format(" ||", ">38"))
    print("|| 5. Add new player." + format(" ||", ">45"))
    print("|| 6. Remove a player." + format(" ||", ">44"))
    print("|| 7. Exit." + format(" ||", ">55"))
    print("# ============================================================== #")


    user_input = 0
    count = 0
    while user_input != 'n':
        usernames_lower_case = []
        usernames = []

        for name in info.items():
            usernames_lower_case.append(name[0].lower())
            usernames.append(name[0])
        
        if count > 0:
            user_input = input("\nWould you like to continue? Yes(y) | No(n).\n :: ")
            
            if user_input == 'n' or user_input == 'N':
                break
            print("\nEnter next command.")
            print()
            x = 'Commands'
            x = x.center(60)
            print("# ============================================================== #")
            print("|| " + x + " ||")
            print("# ============================================================== #")
            print("|| 1. Current standings" + format(" ||", ">43"))
            print("|| 2. Report match results." + format(" ||", ">39"))
            print("|| 3. Get player match history." + format(" ||", ">35"))
            print("|| 4. Get player statistics." + format(" ||", ">38"))
            print("|| 5. Add new player." + format(" ||", ">45"))
            print("|| 6. Remove a player." + format(" ||", ">44"))
            print("|| 7. Exit." + format(" ||", ">55"))
            print("# ============================================================== #")
        user_input = input(":: ")
        
        if user_input == '666':
            info = rating_override(info,usernames_lower_case,usernames)

        while user_input < '1' or user_input > '7':
            
            user_input = input("Yikes, try again \n:: ")
    
        if user_input == '1':
            current_standings(info)
    
        elif user_input == '2':
            match_results(info,usernames_lower_case,usernames)

        elif user_input == '3':
            get_match_history(info,usernames_lower_case,usernames)

        elif user_input == '4':
            get_player_stats(info,usernames_lower_case,usernames)

        elif user_input == '5':
            info = add_player(info,usernames_lower_case)
    
        elif user_input == '6':
            info = remove_player(info, usernames)
        
        elif user_input == '7':
            break
        
        count += 1


main()