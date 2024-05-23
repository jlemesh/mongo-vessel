import pandas as pd
from pymongo import MongoClient
from multiprocessing import Pool
import gc


# insert data into MongoDB
def insert_data(data_dict):
  print('Inserting chunk ...')
  client = MongoClient('mongodb://localhost:27017')
  db = client['vessels']
  collection = db['data']
  chunk_size = len(data_dict) // 32
  data_chunks = [data_dict[i:i+chunk_size] for i in range(0, len(data_dict), chunk_size)]
  del data_dict
  gc.collect()
  for chunk in data_chunks:
    collection.insert_many(chunk, bypass_document_validation=True)
    print('Chunk inserted.')
    del chunk
    gc.collect()
  print('Data inserted.')
  client.close()

data = pd.read_csv('data/aisdk-2023-05-01.csv')

print(data.head(10))
input("Press Enter to continue...")
print('Inserting data into MongoDB...')
data_dict = data.to_dict(orient='records')

del data
gc.collect()

print('Made dictionary.')
num_processes = 512
chunk_size = len(data_dict) // num_processes
data_chunks = [data_dict[i:i+chunk_size] for i in range(0, len(data_dict), chunk_size)]

del data_dict
gc.collect()

print('Inserting chunks...')
client = MongoClient('mongodb://localhost:27017')
db = client['vessels']
collection = db['data']

for chunk in data_chunks:
  collection.insert_many(chunk, bypass_document_validation=True)
  print('Chunk inserted.')
  del chunk
  gc.collect()

print('Data inserted.')
client.close()

# print('Map pool...')
# pool.map(insert_data, data_chunks)
# pool.close()
# pool.join()
print('Done.')
