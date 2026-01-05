#
# Import option data from CSV files into the database
#
# Usage: python3 import_options.py <db_host_name> <path_to_csv_directory>
#
# This script assumes that the source data files are in CSV format with the following columns:
#   time, current, volume, high, low, money, position, a1_p, b1_p, a1_v, b1_v, contract_code
# And data lines like:
#   20251105133000.5, 4199.0, 1.0, 4199.0, 4199.0, 62985.0, 3.0, 5845.0, 2672.5, 1.0, 1.0, AG2512C7100.XSGE
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
temp_table = f'Futures.OptionsTick_temp_{rand_str}'

def import_file(host, file_d: str):
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
        return
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
        "INSERT INTO Futures.OptionsTick "
        "WITH parseDateTime64BestEffort(time, 3) AS parsed_time "
        "SELECT "
        "  toDateTime(parsed_time) AS datetime, "
        "  toMillisecond(parsed_time) AS millisecond, "
        "  upper(substring(contract_code, 1, position(contract_code, '.') - 1)) AS symbol, "
        "  current AS last_price, "
        "  toUInt64(volume) AS volume, "
        "  money AS turnover, "
        "  toUInt64(position) AS open_interest, "
        "  b1_p AS bid1_price, "
        "  toUInt64(b1_v) AS bid1_volume, "
        "  a1_p AS ask1_price, "
        "  toUInt64(a1_v) AS ask1_volume "
        f"FROM {temp_table}"
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

def import_options(host, csv_d):
    dir = os.listdir(csv_d)
    for file in dir:
        file_d = os.path.join(csv_d, file)
        if os.path.isfile(file_d): 
            if str.lower(file).endswith('.csv'):
                import_file(host, file_d)
        else:
            import_options(host, file_d)

if __name__ == "__main__":
    # Create temporary table
    cmd = [
        'clickhouse-client',
        '-h', sys.argv[1],
        '--query', 
        f"CREATE TABLE {temp_table} ("
        "`time`     String, "
        "`current`  Decimal64(3), "
        "`volume`   Float64, "
        "`high`     Decimal64(3), "
        "`low`      Decimal64(3), "
        "`money`    Decimal64(3), "
        "`position` Float64, "
        "`a1_p`     Decimal64(3), "
        "`b1_p`     Decimal64(3), "
        "`a1_v`     Float64, "
        "`b1_v`     Float64, "
        "`contract_code` String "
        ") ENGINE = Memory"
    ]
    subprocess.run(cmd)
    import_options(sys.argv[1], sys.argv[2])
    # Drop temporary table
    cmd = [
        'clickhouse-client',
        '-h', sys.argv[1],
        '--multiquery', 
        f"DROP TABLE {temp_table}"
    ]
    subprocess.run(cmd)