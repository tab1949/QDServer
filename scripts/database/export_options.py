# 
# Export options tick data to files.
#
# Usage: python export_options.py <db_host> <output_dir>
#
# Note: Files will be separated by subject contracts.
# 
import os
import sys
import subprocess
from os import path

def export_to_file(host: str, out: str):
    if not path.exists(out):
        os.makedirs(out)
    elif not path.isdir(out):
        raise Exception(f"Output path {out} is not a directory")
    cmd = [
        'clickhouse-client',
        '-h', host,
        '--query', f"SELECT contract FROM Futures.OptionsTick GROUP BY contract ORDER BY contract"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    contract_res = result.stdout
    contracts = contract_res.strip().split('\n')
    print(f'{contracts.__len__()} contracts in total.')
    input("Continue? (press Enter to continue)")
    for i, contract in enumerate(contracts, 1):
        print(f'({i}/{len(contracts)}) Exporting contract {contract}...')
        out_file = path.join(out, f'{contract}.csv')
        cmd = [
            'clickhouse-client',
            '-h', host,
            '--query', f"SELECT * FROM Futures.OptionsTick WHERE contract='{contract}' ORDER BY datetime FORMAT CSVWithNames"
        ]
        with open(out_file, 'w') as f:
            subprocess.run(cmd, stdout=f, text=True)

if __name__ == "__main__":
    export_to_file(sys.argv[1], sys.argv[2])