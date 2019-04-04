from DataHandler import DataHandler
from tkinter import *

def main():

    dataHandler = DataHandler()

    if dataHandler.num_players == 0:
        print("\n# ============================================================ #")
        print("There are no registered users. Start by adding two new players.")
        print("# ============================================================ #")
        dataHandler.add_player(1)
        dataHandler.add_player(2)

    elif dataHandler.num_players == 1:
        print("\n# ============================================================ #")
        print("There is only one registered user. Add one more player.")
        print("# ============================================================ #")
        dataHandler.add_player(1)

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
            dataHandler.current_standings()
    
        elif user_input == '2':
            dataHandler.report_match()

        elif user_input == '3':
            dataHandler.get_match_history()

        elif user_input == '4':
            dataHandler.get_player_stats()

        elif user_input == '5':
            dataHandler.add_player()
    
        elif user_input == '6':
            dataHandler.remove_player()
        
        elif user_input == '7':
            break
        
        count += 1


main()