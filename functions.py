import configparser
import os
import filecmp
from filecmp import dircmp

"""
Set installation directory
"""
install_dir = 'D:\\Files\\Programming\\Python\\my_projects\\PyFile\\'

"""
Set configuration parser and file
"""
config = configparser.ConfigParser()
config.read(install_dir+'config.ini')

"""
Menu choice functions

The name of each function designates the type of files being manipulated.
Each of these functions utilizes the config file (config.ini) and loops through it to accomplish their given tasks.
"""

def anki():
    anki_choice = int(input('\nPress 1 to copy only new files.\nPress 2 to delete old files and refill the directory.: '))
    if anki_choice == 1: # 'del_dst_dir' flag used to clear backup files, which would accumulate otherwise
        for directory in config['Dirs']:
            copy_dirs(config['Sources']['Anki'], config['Dirs'][directory], dst_sub='Flashcards\\Anki', del_dst_dir='backups')
        finished()

    elif anki_choice == 2:
        for directory in config['Dirs']:
            copy_dirs(config['Sources']['Anki'], config['Dirs'][directory], dst_sub='Flashcards\\Anki', del_dst_dir='backups', fresh=True)
        finished()

def books(copy_configs=False):
    # Look for folders that do not match the home book folder and delete them
    for directory in config['Dirs']:
        compare_delete(config['Dirs']['Files'], config['Dirs'][directory], src_sub='Books\\Calibre')
        copy_dirs(config['Dirs']['Files'], config['Dirs'][directory], src_sub='Books\\Calibre', dst_sub='Books\\Calibre')
    # Copy Calibre configuration files
    if copy_configs == True:
        for directory in config['Dirs']:
            copy_dirs(config['Sources']['Calibre Config'], config['Dirs'][directory], dst_sub='Books\\Config', fresh=True)
    finished()
    
def chrome():
    for directory in config['Dirs']:
        copy_dirs(config['Sources']['Chrome'], config['Dirs'][directory], dst_sub='Browsers\\Chrome', fresh=True)
    finished()

def dropbox():
    copy_warn('Dropbox')
    for directory in config['Dropbox Dirs']:
        copy_dirs(config['Dirs']['Files'], config['Dirs']['Dropbox'], src_sub=config['Dropbox Dirs'][directory], dst_sub=config['Dropbox Dirs'][directory])
    finished()
    

def ext_HDs():
    copy_warn('your external HDs')
    copy_dirs(config['Dirs']['Dropbox'], config['Dirs']['Files'], src_sub='Camera Uploads', dst_sub='Media\\Dropbox Photos')
    copy_dirs(config['Dirs']['Dropbox'], config['Dirs']['Files'], src_sub='Music',  dst_sub='Music')
    copy_dirs(config['Dirs']['Files'], config['Dirs']['External HD 1'])
    copy_dirs(config['Dirs']['Files'], config['Dirs']['External HD 2'])
    copy_dirs(config['Dirs']['Files'], config['Dirs']['Thumb Drive'], src_sub='Books/Calibre', dst_sub='Books\\Calibre')
    copy_dirs(config['Dirs']['Files'], config['Dirs']['Thumb Drive'], src_sub='Documents', dst_sub='Documents')
    copy_dirs(config['Dirs']['Files'], config['Dirs']['Thumb Drive'], src_sub='Programming', dst_sub='Programming')
    finished()

def server():
    for directory in config['Dirs']:
        copy_dirs(config['Sources']['Server'], config['Dirs'][directory], dst_sub='Documents\\Server', fresh=True)
    finished()

def sync_apps():
    copy_dirs(config['Dirs']['Dropbox'], config['Dirs']['Files'], dst_sub='Apps', src_sub='Apps', fresh=True)
    copy_dirs(config['Dirs']['Dropbox'], config['Dirs']['External HD 1'], dst_sub='Apps', src_sub='Apps', fresh=True)
    copy_dirs(config['Dirs']['Dropbox'], config['Dirs']['External HD 2'], dst_sub='Apps', src_sub='Apps', fresh=True)
    copy_dirs(config['Dirs']['Dropbox'], config['Dirs']['Thumb Drive'], dst_sub='Apps', src_sub='Apps', fresh=True)
    finished()

"""
Function for copying directories

'fresh' flag for indicating that the destination needs to be deleted
'sub' flags for designating a subdirectory to work from
'del_dst_dir' flag for indicating that a destination subdirectory needs to be deleted
"""

def copy_dirs(src, dst, src_sub='', dst_sub='', del_dst_dir='', fresh=False):
    if src_sub != '':
        src = src + '\\' + src_sub
    if dst_sub != '':
        dst = dst + '\\' + dst_sub
    if del_dst_dir != '':
        os.system("""rmdir "{0}" /S /Q""".format(dst + '\\' + del_dst_dir))
    if fresh == False:
        os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))
    elif fresh == True:
        os.system("""rmdir "{0}" /S /Q""".format(dst))
        os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))
        
"""
Function for deleting a file and replacing it with another
"""

def refresh_file(src, dst):
    os.system('del "{0}" /Q'.format(dst))
    os.system("""xcopy /Y /I "{0}" "{1}" """.format(src, dst))


"""
Function for deleting a single file
"""

def del_file(dst):
    os.system('del "{0}" /Q'.format(dst))

"""
Function for comparing directories
"""
def dir_compare(src, dst, return_src=False):
    comparison1 = dircmp(src, dst)
    if return_src == False:
        return comparison1.right_only
    elif return_src == True:
        return comparison1.left_only

"""
Function for deleting differences between two directories
"""
def compare_delete(src, dst, src_sub='', dst_sub=''):
    if src_sub != '':
        src = src + '\\' + src_sub
    if dst_sub != '':
        dst = dst + '\\' + dst_sub
    folder_differences = dir_compare(src, dst)
    for folders in folder_differences:
        os.system("""rmdir "{0}" /S /Q""".format(dst + '\\' + folders))


"""
All finished message
"""

def finished():
    print("\nAll done!  Returning to main menu...\n")
    input()


# Warning before copying
def copy_warn(dst):
    print('\nFiles are about to be copied to %s.' % dst)
    print('Press any key to continue...\n')
    input()
