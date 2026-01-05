#
# This script lists options to be imported or ignored.
#
# Usage: python3 list_options.py <path_to_csv_directory>
#

import os
import os.path
import sys
import random
import string

rand_str = ''.join(random.choices(string.ascii_letters, k = 16))
temp_table = f'Futures.OptionsTick_temp_{rand_str}'

def import_file(file_d: str):
    if file_d.find("沪深") != -1 \
    or file_d.find("中证") != -1 \
    or file_d.find("深证") != -1 \
    or file_d.find("上证") != -1 \
    or file_d.find("科创") != -1 \
    or file_d.find("创业") != -1 \
    or file_d.find("E1O") != -1 \
    or file_d.find("E3O") != -1 \
    or file_d.find("E5O") != -1 \
    or file_d.find("E5CO") != -1 \
    or file_d.find("E10O") != -1 \
    or file_d.find("HBE") != -1 \
    or file_d.find("IC") != -1 \
    or file_d.find("IF") != -1 \
    or file_d.find("IM") != -1 \
    or file_d.find("IH") != -1 \
    or file_d.find("CVE") != -1 \
    or file_d.find("JSE") != -1 \
    or file_d.find("KCE") != -1 \
    or file_d.find("KO") != -1 \
    or file_d.find("NFE") != -1 \
    or file_d.find("YFE") != -1 \
    or file_d.lower().find("etf") != -1:
        print("Ignore file: " + file_d)
        with open('./options_ignored.txt', 'a') as f:
            f.write(file_d + '\n')
        return
    print("Import file: " + file_d)
    with open('./options_import.txt', 'a') as f:
        f.write(file_d + '\n')

def import_options(csv_d):
    dir = os.listdir(csv_d)
    for file in dir:
        file_d = os.path.join(csv_d, file)
        if os.path.isfile(file_d): 
            if str.lower(file).endswith('.csv'):
                import_file(file_d)
        else:
            import_options(file_d)

if __name__ == "__main__":
    import_options(sys.argv[1])