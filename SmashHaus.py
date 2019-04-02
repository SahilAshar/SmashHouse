from Player import Player
from DataHandler import DataHandler

def main():

    inf = open("information.csv", "r")
    dataHandler = DataHandler()


    num_players = inf.readline().strip()
    num_players = int(num_players[0])

    # Create a list to store every player object

    player_list = []

    for i in range(num_players):
       
        # Create player objects and store them in player_list

        x = inf.readline().strip()
        x = x.split(",")
        user = Player(x[0],x[1],int(x[2]),int(x[3]),int(x[4]),int(x[5]))
        print(user.username)
        player_list.append(user)
        user_data[x[0]] = user

    # Generate a list of lowercase usernames for verification later

    lower_usernames = []

    for i in range(len(player_list)):
        lower_usernames.append(player_list[i].username.lower())

    if num_players == 0:
        print("\n# ============================================================ #")
        print("There are no registered users. Start by adding two new players.")
        print("# ============================================================ #")
        
        player_list.append(add_player(lower_usernames, num_players))
        user_data[player_list[0].username] = player_list[0]

        num_players += 1

        # Reset lower_usernames such that the second player can't duplicate the first.

        lower_usernames = []

        for i in range(len(player_list)):
            lower_usernames.append(player_list[i].username.lower())
        
        player_list.append(add_player(lower_usernames, num_players))
        user_data[player_list[1].username] = player_list[1]

    elif num_players == 1:
        print("\n# ============================================================ #")
        print("There is only one registered user. Add one more player.")
        print("# ============================================================ #")
        player_list.append(add_player(lower_usernames, num_players))
        user_data[player_list[1].username] = player_list[1]
        num_players += 1


    print(user_data)
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
        lower_usernames = []
        usernames = []

        for i in range(len(player_list)):
            lower_usernames.append(player_list[i].username.lower())
            usernames.append(player_list[i].username)
        
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
        
        #if user_input == '666':
        #    info = rating_override(info,usernames_lower_case,usernames)

        valid = ['1','2','3','4','5','6','7']

        while user_input not in valid:
            
            user_input = input("Yikes, try again \n:: ")
    
        if user_input == '1':
            current_standings(player_list)
    
        elif user_input == '2':
            match_results()

        elif user_input == '3':
            get_match_history()

        elif user_input == '4':
            get_player_stats()

        elif user_input == '5':
            info = add_player()
    
        elif user_input == '6':
            info = remove_player()
        
        elif user_input == '7':
            break
        
        count += 1

main()