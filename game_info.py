import csv
from operator import itemgetter


MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
      
        
        
def open_file(s):
    """opens file propted by user input"""
    present = False
    file_name = input('\nEnter {} file: '.format(s))
    # continues to prompt for file unit a valid one is input
    while present == False:
        try:
           # tries to pen and read the file and asigns the file to a pointer
            fp = open(file_name , encoding="utf-8")
            present = True
        # if the file is not found the user is asked for a differnt input
        except FileNotFoundError:
            print ('\nNo Such file')
            file_name = input('\nEnter {} file: '.format(s))
    return fp

def read_file(fp_games):
    """Reads game data from a CSV file and stores it in a dictionary.

    Args:
        fp_games (file object): Opened game CSV file.

    Returns:
        dict: A dictionary with game names as keys and game details as values.
    """
    # makes reader for the csv
    reader = csv.reader(fp_games)
    # skips header
    next(reader,None)
    # creates empty dict to add key:value pairs to
    final_dict = {}
    # goes through each game in the file
    for line in reader:
        # assigns value for name and realse date
        name = line[0]
        r_date = line[1]
        # splits at semicolins to make lists 
        devs = line[2].split(';')
        genre = line[3].split(';')
        mode = line[4].split(';')
        # if the value of the first genre is multi-player then mode is 0
        # otherwise it is 1
        if mode[0].lower()=='multi-player':
            mode = 0
        else:
            mode = 1
        # if the price is a number it is converted from rupees to USD 
        try:
            price = float(line[5].replace(',', ''))*.012
        # otherwise the game is free
        except:
            price = 0.0
        overall_rev = line[6]
        rev = int(line[7])
        #removes % to int the value
        per_pos = int(line[8].replace('%', ''))
        support = []
        # checks to see if the OS is supported by the game and is it is the 
        # OS is added to the support list
        if int(line[9]) == 1:
            win_sup = 'win_support'
            support.append(win_sup)
        if int(line[10]) == 1:
            mac_sup = 'mac_support'
            support.append(mac_sup)
        if int(line[11]) == 1:
            lin_sup = 'lin_support'
            support.append(lin_sup)
        # adds key:val pairs to the final_dict
        final_dict[name] = [r_date,devs,genre,mode,price,overall_rev,rev,\
        per_pos,support]
    return final_dict
     
    

def read_discount(fp_discount):
    """Reads discount data from a CSV file and stores it in a dictionary.

    Args:
        fp_discount (file object): Opened discount CSV file.

    Returns:
        dict: A dictionary with game names as keys and discount percentages as values.
    """
    # makes reader for the csv
    reader = csv.reader(fp_discount)
    # skips header
    next(reader,None)
    # creates empty dict to add key:value pairs to
    final_dict = {}
    # goes through each game in the file
    for line in reader:
        title = line[0]
        # floats and rounds discount to 2 decimals
        discount = round(float(line[1]),2)
        # adds key:val pair
        final_dict[title] = discount
    return final_dict

def in_year(master_D,year):
    """Filters games by their release year.

    Args:
        master_D (dict): Dictionary containing game data.
        year (int): The year to filter the games by.

    Returns:
        list: A list of games released in the specified year.
    """
    final_list = []
    # makes a list of keys
    list_of_keys = list(master_D.keys())
    # makes a list of values
    list_of_vals = master_D.values()
    # itterates through values
    for i,value in enumerate(list_of_vals):
        # if the last 4 digits of the date are equal to the year the nthe game 
        # is added to the final list
        date = value[0]
        game_year = int(date[-4]+date[-3]+date[-2]+date[-1])
        if game_year == year:
            final_list.append(list_of_keys[i])
    # sorts by alphebetical order
    final_list.sort()
    return final_list

def by_genre(master_D,genre): 
    """Filters games by genre and sorts them by rating.

    Args:
        master_D (dict): Dictionary containing game data.
        genre (str): The genre to filter games by.

    Returns:
        list: A list of games matching the genre, sorted by rating.
    """
    final_list = []
    tup_list = []
    # Makes a list of key val pairs
    list_of_item = list(master_D.items())
    # makes of a list of games
    list_of_keys = list(master_D.keys())
    # iterates through key:value tuples 
    for i,game in enumerate(list_of_item):
        # finds list of genres for the game
        game_gen = game[1][2]
        # if the genre from the user is in the game the game is added to a tup
        # along with the rating
        if genre in game_gen:
            tup = list_of_keys[i] , game[1][7]
            # add the tuples to a list
            tup_list.append(tup)
    # sorts the list by the rating in descending order
    tup_list.sort(key = itemgetter(1),reverse = True)
    # appends each title from the sorted tuple list to make the final list
    for tup in tup_list:
        final_list.append(tup[0])
    return final_list

def by_dev(master_D,developer): 
    """Filters games by developer and sorts them by release year.

    Args:
        master_D (dict): Dictionary containing game data.
        developer (str): The developer to filter games by.

    Returns:
        list: A list of games by the specified developer, sorted by year.
    """
    final_list = []
    tup_list = []
    # Makes a list of key val pairs
    list_of_item = list(master_D.items())
    # makes of a list of games
    list_of_keys = list(master_D.keys())
    # iterates through key:value tuples 
    for i,game in enumerate(list_of_item):
        # finds list of devs for the game
        game_devs = game[1][1]
        # if the dev from the user is in the game the game is added to a tup
        # along with the rating
        if developer in game_devs:
            date = game[1][0]
            game_year = int(date[-4:])
            tup = list_of_keys[i] , game_year 
            # add the tuples to a list
            tup_list.append(tup)
    # sorts the list by the year in descending order
    tup_list.sort(key = itemgetter(1),reverse = True)
    # appends each title from the sorted tuple list to make the final list
    for tup in tup_list:
        final_list.append(tup[0])
    return final_list

def per_discount(master_D,games,discount_D): 
    """Finds the discounted price for games if applicable.

    Args:
        master_D (dict): Dictionary containing game data.
        games (list): List of games to find discounts for.
        discount_D (dict): Dictionary of discount data.

    Returns:
        list: A list of discounted prices for the specified games.
    """
    final_list = []
    tup_list = []
    # Makes a list of key val pairs
    list_of_item = list(master_D.items())
    # makes of a list of games
    list_of_keys = list(master_D.keys())
    # iterates through key:value tuples 
    for i,game in enumerate(list_of_item):
        # if the title of the gmae is in the user specified games
        if list_of_keys[i] in games:
            try:
                # seeing if a discount is avalibe for the game by using the game
                # as the key in the discount dictionary
                game_discount = discount_D[list_of_keys[i]]
                discounted_price = round(((1-(game_discount/100))*game[1][4]),6)
            except:
                # if its not in the dictionary of discounted games the price 
                # reamins teh same
                discounted_price = game[1][4]
            # making tup with game and new price
            game_price = list_of_keys[i],discounted_price
            tup_list.append(game_price)
   # for the games in user specified games 
    for g in games:
        # goes  through each tup in tup_list and checks if the game is in
        # the tuple
        for tup in tup_list:
            if g.lower() == tup[0].lower():
                # if so the discounted price is added to the list
                final_list.append(tup[1])
                break
    return final_list   

def by_dev_year(master_D,discount_D,developer,year):
    """Find games by a developer in a specific year and sort by price.

    Args:
        master_D (dict): Dictionary of game data.
        discount_D (dict): Dictionary of discount data.
        developer (str): The developer to filter by.
        year (int): The release year to filter by.

    Returns:
        list: List of games by the developer in the specified year, sorted by price.
    """
    final_list = []
    tup_list = []
    valid_games = []
    # gets games by the specified developer
    list_of_game=by_dev(master_D, developer)
    # gets games by developer
    list_of_year = in_year(master_D, year)
    for game in list_of_game:
        # if the games in by devs are als o in the in year list they are added 
        # to valid games 
        if game in list_of_year:
            valid_games.append(game)
        else:
            continue
    # finds discounts for valid games 
    list_of_discounts = per_discount(master_D,valid_games, discount_D)
    for i,g in enumerate(valid_games):
        # makes a tuple with the game title and price
        game_price = g,list_of_discounts[i]
        tup_list.append(game_price)
    # sorts by alphebtical order of title
    tup_list.sort(key=itemgetter(0))
    # sorts by value of price (low-high)
    tup_list.sort(key=itemgetter(1))
    for tup in tup_list:
        # adds each game to the final list
        final_list.append(tup[0])
    return final_list


          
def by_genre_no_disc(master_D,discount_D,genre):
    """Find games of a specific genre without discounts.

    Args:
        master_D (dict): Dictionary of game data.
        discount_D (dict): Dictionary of discount data.
        genre (str): The genre to filter by.

    Returns:
        list: List of games in the specified genre without discounts, sorted by price.
    """      
    final_list = []
    valid_games = []
    list_of_tups = []
    # list of discounted games
    offered_discounts = list(discount_D.keys())
    # filters games by genre
    genre_game = by_genre(master_D, genre)
    for game in genre_game:
       # if the game is discounted skip it
        if game in offered_discounts:
            continue
        # otherwise add the game to valid games
        else:
            valid_games.append(game)
    for g in list(master_D.items()):
        # if the game title is in valid games get the data used to sort the 
        # tuples
        if g[0] in valid_games:
            tup = g[0],g[1][4], g[1][7]
            list_of_tups.append(tup)
        else: 
            continue
    # sort by percent positve reviews (high-low)
    list_of_tups.sort(key = itemgetter(2), reverse = True)
    # sort by price (low-high)
    list_of_tups.sort(key = itemgetter(1))
    for tup in list_of_tups:
        # add the title to the lsit
        final_list.append(tup[0])
    return final_list
            

def by_dev_with_disc(master_D,discount_D,developer):
    """Find games by a developer with discounts and sort by price.

    Args:
        master_D (dict): Dictionary of game data.
        discount_D (dict): Dictionary of discount data.
        developer (str): The developer to filter by.

    Returns:
        list: List of games by the developer with discounts, sorted by price.
    """
    final_list = []
    valid_games = []
    list_of_tups = []
    # list of discounted games
    offered_discounts = list(discount_D.keys())
    # filters games by dev
    dev_game = by_dev(master_D, developer)
    for game in dev_game:
        # if the game is discounted add it
        if game in offered_discounts:
            valid_games.append(game)
        # otherwise skip it
        else:
            continue
    # for each game 
    for g in list(master_D.items()):
        # if the gmae is valid
        if g[0] in valid_games:
            # amke a tuple with info that coesponds to the title
            tup = g[0],g[1][4], int(g[1][0][-4:])
            list_of_tups.append(tup)
        else: 
            continue
    # sort the list by the oldest to newest
    list_of_tups.sort(key = itemgetter(2))
    # sorts the list from cehapies to most expensive
    list_of_tups.sort(key = itemgetter(1))
    for tup in list_of_tups:
        final_list.append(tup[0])
    return final_list
            
            
             
def main():
    # gets game and discount files
    user_game_file = read_file(open_file('games'))
    user_disc_file = read_discount(open_file('discount'))
    # makes a list of valid user inputs
    valid_numbers = '1','2','3','4','5','6','7'
    # asks user for their input
    user_input = input(MENU)
    # sete the stop looping condition to false
    stop = False
    while stop == False:
       # if user inputs 1
        if user_input == '1':
            # user enters a year
            user_year = input('\nWhich year: ')
            valid = False
            while valid == False:
                try:
                    # tries to int the year and valid becomes ture
                    user_year = int(user_year)
                    valid = True
                    games_by_year = in_year(user_game_file,user_year)
                    # if the list is not empty it prints the year
                    if len(games_by_year)>0:
                        print("\nGames released in {}:".format(str(user_year)))
                        # seperates list of games by a comma followed by a space
                        print(', '.join(games_by_year))
                    else:
                        print("\nNothing to print")
                # if the year is not a number it will need a new input
                except:
                    print("\nPlease enter a valid year")
                    user_year = input('\nWhich year: ')
            # asks user for new input
            user_input = input(MENU)
        if user_input == '2':
            # asks user for dev name
            user_dev = input('\nWhich developer: ')
            # list of gamews by dev
            list_of_games = by_dev(user_game_file, user_dev)
            if len(list_of_games)>0:
                # prints games made by the dev seperated by a comma and space
                print("\nGames made by {}:".format(user_dev))
                print(', '.join(list_of_games))
            else:
                # if there list is empty it says nothign to print
                print("\nNothing to print")
            # asks user for a nuew input
            user_input = input(MENU)
        if user_input == '3':
            # gers users inputed genre
            user_genre = input ('\nWhich genre: ' )
            # makes a list of games in a gnere
            list_of_games = by_genre(user_game_file, user_genre)
            if len(list_of_games)>0:
               # prints the games of the spevified genre seperated by a comma
               # and a space
                print("\nGames with {} genre:".format(user_genre))
                print(', '.join(list_of_games))
            else:
                # if there is nothing to print, the user is notified
                print("\nNothing to print")
            user_input = input(MENU)
        if user_input =='4':
            # gets the users desired dev
            user_dev = input('\nWhich developer: ')
            # gets the users desired release year
            user_year = input('\nWhich year: ')
            # sets a looping conditon to false
            valid = False
            while valid == False:
                try:
                    # tries to int the year
                    user_year = int(user_year)
                    # if the year is a number the loop can end
                    valid = True
                    # gets games by the devloper in the desired year
                    games_by_dev_year = by_dev_year(user_game_file,\
                    user_disc_file,user_dev,\
                             user_year)
                    if len(games_by_dev_year)>0:
                        # if the list of gams has content it is printed
                        print("\nGames made by {} and released in {}:".format\
                              (user_dev,str(user_year)))
                       # seprates by comma and space
                        print(', '.join(games_by_dev_year))
                    else:
                        print("\nNothing to print")
                except ValueError:
                    # if the yera cannot be converted to int the user must 
                    #  input a new year
                    print("\nPlease enter a valid year")
                    user_year = input('\nWhich year: ')
           # user can input a new option
            user_input = input(MENU)
        if user_input == '5':
            # gets the users desired genre
            user_genre = input('\nWhich genre: ')
            # finds games of the genre without a discount
            list_of_no_disc = by_genre_no_disc(user_game_file, user_disc_file,\
            user_genre)
            if len(list_of_no_disc)>0:
                # displays the games seperated by a comma and space
                print("\nGames with {} genre and without a discount:".format\
                (user_genre))
                print(', '.join(list_of_no_disc))
            else:
               # if no games meet criteria the user is notified
                print("\nNothing to print")
            # user can input a new option
            user_input = input(MENU)
        if user_input == '6':
            # gets the useres desired developer
            user_dev = input('\nWhich developer: ')
            # finds games by the developer that offer a discount
            list_with_disc = by_dev_with_disc(user_game_file, user_disc_file,\
            user_dev)
            if len(list_with_disc)>0:
                # prints games seperated by spaces and commas
                print("\nGames made by {} which offer discount:".format\
                (user_dev))
                print(', '.join(list_with_disc))
            else:
                # if no games meet criteria the user is notified
                print("\nNothing to print")
            user_input = input(MENU)
        if user_input == '7':
            # when the user wants to quit the stop looping condition is cahnged
            # to True and the loop breaks
            stop = True
        if user_input not in valid_numbers:
            # if the input is not in the valid options th user is notified and 
            # prompted to input again
            print("\nInvalid option")
            user_input = input(MENU)

     # thanks the user     
    print("\nThank you.")
if __name__ == "__main__":
    main()

