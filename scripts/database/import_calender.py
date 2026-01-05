#
# Import calendar data from CSV files into the database
#
# Usage: python3 import_calender.py <db_host_name> <path_to_csv_directory>
#
# This script assumes that the source data files are in CSV format with the following columns:
#   exchange, cal_date, is_open, pretrade_date
#
# Note: This script creates a temporary table for importing data.
#
import os
import os.path
import subprocess
import sys
import random
import string

rand_str = ''.join(random.choices(string.ascii_letters, k = 16))
temp_table = f'Futures.TradingCalendar_temp_{rand_str}'

def import_file(host, file_d):
    print("Importing file: " + file_d)
    # Load raw data into temporary table
    cmd = [
        'clickhouse-client',
        '-h', host,
        '--multiquery', 
        f"INSERT INTO {temp_table} FORMAT CSVWithNames"
    ]
    with open(file_d, 'r') as source_file:
        subprocess.run(cmd, stdin=source_file)
    # Transform and insert into final table
    cmd = [
        'clickhouse-client',
        '-h', host,
        '--multiquery', 
        "INSERT INTO Futures.TradingCalendar "
        "SELECT "
        "exchange, "
        "toDate(cal_date) AS date, "
        "is_open AS is_open, "
        "toDate(pretrade_date) AS pre_trading_day "
        f"FROM {temp_table} WHERE pretrade_date != ''"
    ]
    subprocess.run(cmd)
    # Clear temporary table
    cmd = [
        'clickhouse-client',
        '-h', host,
        '--multiquery', 
        f"TRUNCATE TABLE {temp_table}"
    ]
    subprocess.run(cmd)

def import_calender(host, csv_d):
    dir = os.listdir(csv_d)
    for file in dir:
        file_d = os.path.join(csv_d, file)
        if os.path.isfile(file_d): 
            if str.lower(file).endswith('.csv'):
                import_file(host, file_d)
        else:
            import_calender(host, file_d)

if __name__ == "__main__":
    # Create temporary table
    cmd = [
        'clickhouse-client',
        '-h', sys.argv[1],
        '--query', 
        f"CREATE TABLE {temp_table} ("
        "`exchange` String,"
        "`cal_date` String,"
        "`is_open` UInt8,"
        "`pretrade_date` String"
        ") ENGINE = Memory"
    ]
    subprocess.run(cmd)
    import_calender(sys.argv[1], sys.argv[2])
    # Drop temporary table
    cmd = [
        'clickhouse-client',
        '-h', sys.argv[1],
        '--multiquery', 
        f"DROP TABLE {temp_table}"
    ]
    subprocess.run(cmd)