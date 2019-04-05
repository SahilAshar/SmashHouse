from Player import Player
import math
import csv

def check_cancel(n):
    if n.lower() == 'cancel':
        return True
    else:
        return False

class DataHandler():

    def __init__(self):
        self.inf = open("information.csv", "r")
        self.out = open("information.csv", "a")
        self.his_in = open("match_history.csv", "r")
        self.his_out = open("match_history.csv", "a")
        self.read_num_players(self.inf)
        if self.num_players >= 1:
            self.build_player_list(self.num_players)
        else:
            self.player_list = []
            self.user_data = {}
            self.lower_usernames = []

    def read_num_players(self, inf):
        self.num_players = inf.readline().strip()
        self.num_players = int(self.num_players[0])

    def build_player_list(self, num_players):
        
        self.user_data = {}
        self.player_list = []
        self.lower_usernames = []

        for i in range(self.num_players):
       
        # Create player objects and store them in player_list

            x = self.inf.readline().strip()
            x = x.split(",")
            user = Player(x[0],x[1],int(x[2]),int(x[3]),int(x[4]),int(x[5]))
            self.player_list.append(user)
            self.user_data[x[0]] = user

        for i in range(len(self.player_list)):
            self.lower_usernames.append(self.player_list[i].username.lower())

    def add_to_user_data(self, player_object):
        self.user_data[player_object.username] = player_object

    def add_to_player_list(self, player_object):
        self.player_list.append(player_object)

    def add_to_lower_usernames(self, player_list):
        x = len(player_list) - 1
        self.lower_usernames.append(player_list[x].username.lower())

    def current_standings(self): # Done
        
        name_rank = []

        if len(self.player_list) == 0:
            print("There are no registered users.")
            return

        for names in self.user_data.items():
            temp = []
            temp.append(names[0])
            temp.append(int(names[1].rating))
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

    def report_match(self): # Done
        
        if len(self.player_list) == 0:
            print("There are no registered users.")
            return
        
        print("\nHere is a list of players.")
        count = 1
        for i in range(len(self.player_list)):
            
            if count == 1:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
            
                count += 1

            elif count % 3 != 0:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
                count += 1
            else:
                print(str(count) + ")", end = " ")
                print(self.player_list[i].username)
                count += 1

        if count % 3 != 0:
            print("\n\nEnter the usernames of the players that played.")
        
        else:
            print("\nEnter the usernames of the players that played.")

        player1 = input("Player 1 :: ")
        check = check_cancel(player1)
        if check == True:
            return
        while player1.lower() not in self.lower_usernames:
            print("Player not found. Try again.")
            player1 = input("Player 1 :: ")
            check = check_cancel(player1)
            if check == True:
                return

        player2 = input("Player 2 :: ")
        check = check_cancel(player2)
        if check == True:
            return
        while player2.lower() not in self.lower_usernames:
            print("Player not found. Try again.")
            player2 = input("Player 2 :: ")
            check = check_cancel(player2)
            if check == True:
                return

        players = [player1.lower(),player2.lower()]
        player1 = self.player_list[self.lower_usernames.index(player1.lower())].username
        player2 = self.player_list[self.lower_usernames.index(player2.lower())].username

        print("\nWho won the match?", player1,"or", player2 + "?")
        result = input(" :: ")
        check = check_cancel(result)
        if check == True:
            return
        while result.lower() not in players:
            print("Please enter a valid response.")
            result = input(" :: ")
            check = check_cancel(result)
            if check == True:
                return

        print("\nWhat was the score? Enter the number associated with the score.")
        print("1) 2-0\n2) 2-1")
        score = input(" :: ")
        check = check_cancel(score)
        if check == True:
            return
        while score < '1' or score > '2':
            print("Please enter a valid response.")
            score = input(" :: ") 
            check = check_cancel(score)
            if check == True:
                return  
        
        if result.lower() == player1.lower():
            result = player1
        else:
            result = player2

        if score == '1':
            score = "2-0"
        else:
            score = "2-1"

        # Add results to match history

        self.his_out = open("match_history.csv", "a")
        self.his_out.write(str(player1) + ',' + str(player2) + ',' + str(result) + ',' + str(score) + "\n")
        self.his_out.close()

        # Run algorithm for updating the player ratings.

        player1_rating = int(self.player_list[self.lower_usernames.index(player1.lower())].rating)
        player2_rating = int(self.player_list[self.lower_usernames.index(player2.lower())].rating)

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


        for i in range(len(self.player_list)):
            if self.player_list[i].username == player1 or self.player_list[i].username == player2:
                if self.player_list[i].username == player1:
                    self.player_list[i].matches_played += 1
                    if player1 == result:
                        self.player_list[i].wins += 1
                        self.player_list[i].rating = player1_rating
                    else:
                        self.player_list[i].losses += 1
                        self.player_list[i].rating = player1_rating
                    self.player_list[i] = Player(player1, self.player_list[i].name,self.player_list[i].rating,self.player_list[i].matches_played, self.player_list[i].wins, self.player_list[i].losses)
                else:
                    self.player_list[i].matches_played += 1
                    if player2 == result:
                        self.player_list[i].wins += 1
                        self.player_list[i].rating = player2_rating
                    else:
                        self.player_list[i].losses += 1
                        self.player_list[i].rating = player2_rating
                    self.player_list[i] = Player(player2, self.player_list[i].name,self.player_list[i].rating,self.player_list[i].matches_played, self.player_list[i].wins, self.player_list[i].losses)

        file1 = open("information.csv", "w")
        temp = str(self.num_players) + ',,,,,\n'

        for i in range(len(self.player_list)):
            temp += self.player_list[i].username + ','
            temp += self.player_list[i].name + ','
            temp += str(self.player_list[i].rating) + ','
            temp += str(self.player_list[i].matches_played) + ','
            temp += str(self.player_list[i].wins) + ','
            temp += str(self.player_list[i].losses) + '\n'

        file1.writelines(temp)
        file1.close()

        return



        # Update ratings in the dictionary

        # Update 'Games' column in the dictionary

        # Update 'Wins' column in the dictionary

    def get_match_history(self): #Done
        
        
        if len(self.player_list) == 0:
            print("There are no registered users.")
            return

        self.his_in = open("match_history.csv", "r")
        
        history_dict = {}
        game = 0

        history = self.his_in.readlines()
        for i in range(len(history)):
            history[i] = history[i].strip()
            history[i] = history[i].split(",")
            history_dict[game] = history[i]
            game += 1
        
        print("\nHere is a list of players.")
        count = 1
        for i in range(len(self.player_list)):
            
            if count == 1:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
            
                count += 1

            elif count % 3 != 0:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
                count += 1
            else:
                print(str(count) + ")", end = " ")
                print(self.player_list[i].username)
                count += 1  

        if count % 3 != 0:
            print("\n\nWho's match history would you like to view? Enter their username.")
        else:
            print("\nWho's match history would you like to view? Enter their username.")

        user_history = input(" :: ")
        check = check_cancel(user_history)
        if check == True:
            return
        while user_history.lower() not in self.lower_usernames:
            print("Please enter a valid username")
            user_history = input(" :: ")
            check = check_cancel(user_history)
            if check == True:
                return

        user_history = self.player_list[self.lower_usernames.index(user_history.lower())].username

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

        self.his_in.close()

        return

    def add_player(self, g = 0): # Done

        if g != 0:
            print("\nPlayer " + str(g) + " :", end = "")

        check = False
        confirm = ''

        while not check:
            username = input("\nEnter your username. \n :: ")
            if username.lower() == 'cancel' and g != 0:
                print("\nEnter a valid username.")
                continue
            
            check = check_cancel(username)
            if check == True and g == 0:
                return
            #Check length
            if len(username) > 12:
                print("\nUsername can't exceed 12 characters.")
                continue
            #Check repeats
            if username.lower() in self.lower_usernames:
                print("\nUsername already taken. Enter a different username.")
                continue
            #Check user validation
            valid = ['y','n']
            confirm = input("\nIs [" + username + "] the username you want? Yes(y) | No(n). \n :: ")
            check = check_cancel(confirm)
            if check == True and g == 0:
                return

            while confirm.lower() not in valid:
                print("\nEnter a valid response.")
                confirm = input("Is [" + username + "] the username you want? Yes(y) | No(n). \n :: ") 
                check = check_cancel(confirm)
                if check == True and g == 0:
                    return
                
            if confirm.lower() == 'n':
                continue
            #If user confirms, exit loop. Move on.
            if confirm.lower() == 'y':
                check = True


        #Do same method for user's name.
        check = False
        while not check:
            name = input("\nEnter your first name and the first initial of your last name. \n :: ")
            if name.lower() == 'cancel' and g != 0:
                print("\nEnter a valid name.")
                continue

            valid = ['y','n']
            confirm = input("\nIs [" + name + "] the correct name? Yes(y) | No(n). \n :: ")
            check = check_cancel(confirm)
            if check == True and g == 0:
                return

            while confirm.lower() not in valid:
                print("\nEnter a valid response.")
                confirm = input("Is [" + name + "] the correct name? Yes(y) | No(n). \n :: ") 
                check = check_cancel(confirm)
                if check == True and g == 0:
                    return
            if confirm.lower() == 'n':
                continue
            if confirm.lower() == 'y':
                check = True


        self.num_players += 1

        file1 = open("information.csv", "r")
        update_players = file1.readlines()
        update_players[0] = (str(self.num_players) +",,,,,\n")
        file1.close()
        file1 = open("information.csv", "w")
        file1.writelines(update_players)
        file1.close()

        print("\nDone")

        x = Player(username,name)
        self.add_to_player_list(x)
        self.add_to_user_data(x)
        self.add_to_lower_usernames(self.player_list)

        # TODO : Update info.csv

        profile = username + ',' + name + ',' + '1200' + ',' + '0' + ',' + '0' + ',' + '0'
        self.out = open("information.csv", "a")
        self.out.write(profile + '\n')
        self.out.close()

        return

    def get_player_stats(self): #Done
        
        if len(self.player_list) == 0:
            print("There are no registered users.")
            return
        
        print("\nHere is a list of players.")
        count = 1
        for i in range(len(self.player_list)):
            
            if count == 1:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
            
                count += 1

            elif count % 3 != 0:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
                count += 1
            else:
                print(str(count) + ")", end = " ")
                print(self.player_list[i].username)
                count += 1

        if count % 3 != 0:
            print("\n\nEnter a player's username.")
        
        else:
            print("\nEnter a player's username.")
            
        user_stats = input(" :: ")
        check = check_cancel(user_stats)
        if check == True:
            return
        while user_stats.lower() not in self.lower_usernames:
            print("Please enter a valid username.")
            user_stats = input(" :: ")
            check = check_cancel(user_stats)
            if check == True:
                return

        user_stats = self.player_list[self.lower_usernames.index(user_stats.lower())].username
        name = self.user_data[user_stats].name
        rating = self.user_data[user_stats].rating
        matches_played = self.user_data[user_stats].matches_played
        wins = self.user_data[user_stats].wins
        losses = self.user_data[user_stats].losses
        if wins != 0 and matches_played != 0:
            winrate = (str(((round(int(wins)/int(matches_played),4)))*100)) + "%"
        elif wins != 0 and losses == 0:
            winrate = str(wins)
        elif wins == 0 and losses != 0:
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
        print("Rating : " + str(rating))
        print("Matches played : " + str(matches_played))
        print("Wins : " + str(wins))
        print("Losses : " + str(losses))
        print("Winrate : " + winrate)

        return

    def remove_player(self): #Done
                
        if len(self.player_list) == 0:
            print("There are no registered users.")
            return

        password = 'FuckSahil'
        
        print("\nHere is a list of players.")
        count = 1
        for i in range(len(self.player_list)):
            
            if count == 1:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
            
                count += 1

            elif count % 3 != 0:
                print(str(count) + ")", end = " ")
                print(format(self.player_list[i].username, "<15"), end = "")
                count += 1
            else:
                print(str(count) + ")", end = " ")
                print(self.player_list[i].username)
                count += 1
        
        if count % 3 != 0:
            print("\n\nEnter the username of the player you would like to remove.")
            print("This area is case sensitive.")
        
        else:
            
            print("\nEnter the username of the player you would like to remove.")
            print("This area is case sensitive.")
        
        user_stats = input(" :: ")
        check = check_cancel(user_stats)
        if check == True:
            return
        while user_stats.lower() not in self.lower_usernames:
            print("Enter a valid username.")
            user_stats = input(" :: ")
            check = check_cancel(user_stats)
            if check == True:
                return

        print("\nThis process requires admin approval.")
        input_password = input("Password :: ")
        check = check_cancel(input_password)
        if check == True:
            return
        while input_password != password:
            print("Invalid password.")
            input_password = input("Password :: ")
            check = check_cancel(input_password)
            if check == True:
                return

        user_stats = self.player_list[self.lower_usernames.index(user_stats.lower())].username

        file2 = open("information.csv", "r")
        file_remove = file2.readlines()

        for i in range(len(file_remove)):
            if user_stats in file_remove[i]:
                file_remove.pop(i)
                self.player_list.pop(i - 1)
                break
        index = 0
        for i in self.lower_usernames:
            if user_stats.lower() == i:
                self.lower_usernames.pop(index)
            index += 1

        self.user_data.pop(user_stats)

        self.num_players -= 1
        temp = str(self.num_players) + ',,,,,\n'
        for i in range(1,len(file_remove)):
            temp += file_remove[i]
        
        file2.close()
        file2 = open("information.csv", 'w')
        file2.write(temp)
        file2.close()

        return