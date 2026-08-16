import sys

import pandas as pd

args = sys.argv
print('args:', args)
for arg in range(1,len(args)):  # the first item (index 0) will always be the name of the script being executed.
    print('args index:', arg, '\n','arg content:', args[arg])

month = args[1]
df = pd.DataFrame({'day': [1,2], 'num_passengers': [3,4]})
df['month'] = month
print(df.head())

df.to_parquet(f"output_{month}.parquet")  # parquet is a binary file used to the content of CSV files in a more compreesed way.

print('hello pipeline')