import json
import os
import filecmp
import shutil
import sys
from os.path import exists
from time import sleep

plat = sys.platform


class JSONRunner:

    @staticmethod
    def copy_dirs(src, dst, subs='', src_sub='', dst_sub=''):
        """
        Searches for and deletes files not found in the source,
        then copies any new files to the destination
        """
        # Join paths (if specified)
        if subs:
            src = os.path.join(src, subs)
            dst = os.path.join(dst, subs)
        if dst_sub:
            dst = os.path.join(dst, dst_sub)
        if src_sub:
            src = os.path.join(src, src_sub)
        print('\nComparing...\n')
        print('\nSource: %s' % src)
        print('Destination: %s\n' % dst)
        for src_root, src_dirs, src_files in os.walk(src, topdown=True):

            dst_root = os.path.join(dst, os.path.relpath(src_root, src))
            dirs = filecmp.dircmp(src_root, dst_root)

            # Find old files and delete them from destination
            for item in dirs.right_only:
                try:
                    print('Removing ' + item)
                except UnicodeEncodeError:
                    # Prevents the program from stopping in the event of an
                    # awkward file name
                    print('Removing file (Unicode error)')
                dst_path = os.path.join(dst_root, item)
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)

            # Find new files and add them to destination
            for item in dirs.left_only:
                try:
                    print('Adding ' + item)
                except UnicodeEncodeError:
                    # Prevents the program from stopping in the event of an
                    # awkward file name
                    print('Adding file (Unicode error)')
                src_path = os.path.join(src_root, item)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, os.path.join(dst_root, item))
                else:
                    shutil.copy2(src_path, os.path.join(dst_root, item))

        # Once clearing and adding has completed, update existing files
        print('\nUpdating: ')
        if plat != 'win32':
            os.system(
                """rsync -r -u -v --links "{0}"/* "{1}" """.format(src, dst))
        else:
            os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))

    # Warning before copying
    def copy_warn(self, dst):
        print('\n%s files are about to be copied..' % dst)
        print('Press any key to continue...\n')
        input()

    @staticmethod
    def routine(JSON_source, routine):
        """Run a backup routine from a JSON file"""

        # List for collection troublesome directories
        dir_errors = []

        with open(JSON_source + '.json') as data_file:
            dir_obj = json.load(data_file)

        base = dir_obj['Routines'][routine]['Setup']['Base Directory']

        for key, value in dir_obj['Routines'][routine].items():
            try:
                if key is not 'Setup':
                    dest = dir_obj['Routines'][routine][key]
                    if type(dest) is not dict:
                        print(dir_obj['Locations'][dest])
                        JSONRunner.copy_dirs(
                            dir_obj['Locations'][base],
                            dir_obj['Locations'][dest]
                        )
            except KeyboardInterrupt:
                print('\nYou have elected to exit the program, goodbye!\n')
                exit()
            except KeyError:
                print('Your JSON contains an incorrect key: {0}'.format(value))
                dir_errors.append(dest)
                sleep(5)
                continue
            except OSError:
                print("""This directory does not exist: {0}
                \nContinuing in 5 seconds...\n
                """.format(dest))
                dir_errors.append(dest)
                sleep(5)
                continue

        if len(dir_errors) > 0:
            print('\nThese directories experienced errors:')
            for i in dir_errors:
                print(i)

print(JSONRunner.routine('test_json', 'Test'))
