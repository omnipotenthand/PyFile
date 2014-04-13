# AceSafe
# By Ace Eddleman, 2014

import db
import dirobj

# User name for welcome message
name = 'User'

# Welcome message
def welcome(name=name):
    print('\nWelcome to your file management program, {0}!'.format(name))
    try:
        rebuild = int(input('\nWould you like to rebuild the database before you begin?\nPress 1 for yes, anything else for no:  '))
        if rebuild == 1:
            db.rebuild_db()
        else:
            pass
    except ValueError:
        pass


"""Start of program"""
if __name__ == '__main__':
    welcome()
    db.DB.create_menu("routines.db")