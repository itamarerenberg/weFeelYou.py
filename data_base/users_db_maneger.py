from data_base import songs_db_maneger

USERS_FILE = './data_base/data/users'
USERS_SONGS_DIR = './data_base/data/users_songs'


def is_user_exist(userName):
    '''
    check if the current user already exists
    :param userName: current user_name
    :return: True if exists
    '''
    with open(USERS_FILE, 'r') as ufile:
        for user in ufile:
            if user == userName:
                return True
    return False


def add_user(userName):
    """
    register a new user
    :param userName: new user's name
    :return: True, None if the user register successful and False, reason (string) otherwise
    """

    if is_user_exist(userName):
        return False, 'reason: user already exist'
    f = open(USERS_FILE, 'a')  # open file in mode 'a' -> open for writing to end of file
    f.write(userName + '\n')
    f.close()

    # create a songs file for the new user
    songs_db_maneger.create_new_songs_file(f'({userName})songs.csv')

    return True, None


