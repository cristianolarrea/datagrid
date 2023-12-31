import sys
sys.path.append('../src/')

from datagrid import DataGrid
import time

n = set([10, 100, 1000, 10000, 30000, 50000, 70000, 100000, 300000, 500000, 20000, 50000, 70000, 200000, 400000])

with open(f'../results/testInsert.csv', 'w') as f:
    f.write('n,time\n')

    for i in n:
        datagrid = DataGrid()

        start_time = time.time()
        datagrid.read_csv(f'../data/fake_data{i}.csv')
        end_time = time.time()

        print(f"Time to read {i} rows: {end_time - start_time}")
        f.write(f'{i},{end_time - start_time}\n')