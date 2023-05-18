import scripts.recommender as Recommender
import scripts.init as Init
import scripts.user as User
import os
import time


def display_menu():

    os.system('cls')
    print('Movie Recommender System\n')
    print('1 - Search')
    print('2 - Login')
    print('3 - Repair Files')
    print('4 - Clear Cache')
    print('x - Exit\n')
    return input('>> ')


def search_movie():

    os.system('cls')
    print('Search for Movies\n')
    phrase = input('Search : ')

    start_time = time.time()
    movies = Recommender.search(phrase)
    end_time = time.time()

    print('\nResults\n')

    for movie in movies[0:10]:
        print(movie)
    
    time_taken = end_time - start_time

    print('')
    print(f'Time taken : {time_taken}s')
    user_input = input('Press any key to continue (x to exit) >> ')
    
    if user_input == 'x':
        return 1
    else:
        return 0


def user_login():

    os.system('cls')
    print('User Login\n')
    user_id = input('User ID : ')

    try:
        user_id = int(user_id)

        if (user_id >= 0) and (user_id <= 162541):
            user = User.User(user_id)

            start_time = time.time()
            print('\nResults\n')
            for movie in user.recommend():
                print(movie)
            end_time = time.time()
            time_taken = end_time - start_time
            print('')
            print(f'Time taken : {time_taken}s')
            user_input = input('Press any key to continue (x to exit) >> ')
        
        else:
            print('\nUser does not exist')
            user_input = input('Press any key to continue (x to exit) >> ')

    except Exception as e:
        print('')
        print(e)
        user_input = input('Press any key to continue (x to exit) >> ')
    
    if user_input == 'x':
        return 1
    else:
        return 0
    

if __name__ == '__main__':

    while True:
        user_input = display_menu()

        if user_input == 'x':
            break

        elif user_input == '1':
            if search_movie() == 1:
                break

        elif user_input == '2':
            if user_login() == 1:
                break

        elif user_input == '3':
            print('\nFile Repairing might take quite some time')
            user_input = input('Type "yes" to continue: ')
            print('')

            if user_input == 'yes':
                Init.initialize()
            else:
                print('Operation aborted...')
                input('>> ')

        elif user_input == '4':
            print('')
            Init.clear_cache()
            input('Press any key to continue >> ')

        else:
            pass
    
    print('\nThanks you and have a GREAT day ... \n')