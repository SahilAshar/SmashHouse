class DataHandler():

    def __init__(self):
        self.inf = open("information.csv", "r")
        self.num_players = inf.readline().strip()
        self.num_players = int(num_players[0])
        self.out = open("information.csv", "a")

    def current_standings():
        return


    def report_match():
        return


    def get_match_history():
        return


    def add_player(lower_usernames, num_players):
        
        check = False
        confirm = ''

        while not check:
            username = input("\nEnter your username. \n :: ")
            #Check length
            if len(username) > 12:
                print("\nUsername can't exceed 12 characters.")
                continue
            #Check repeats
            if username.lower() in lower_usernames:
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


        num_players += 1

        file1 = open("information.csv", "r")
        update_players = file1.readlines()
        update_players[1] = (str(num_players) +",,,,,\n")
        file1.close()
        file1 = open("information.csv", "w")
        file1.writelines(update_players)
        file1.close()

        print("\nDone")

        return Player(username,name)

    def get_player_stats():
        return


    def remove_player():
        return
