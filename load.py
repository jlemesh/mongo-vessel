import pandas as pd
from pymongo import MongoClient
from multiprocessing import Pool
import gc

def insert_data(data_dict):
  """Insert vessel data into a collection

  Parameters
  ----------
  data_dict : dict
    A dictionary of vessels data

  Returns
  -------
  None
  """
  print('Inserting chunk ...')
  client = MongoClient('mongodb://localhost:27017')
  db = client['vessels']
  collection = db['data']
  chunk_size = len(data_dict) // 100
  data_chunks = [data_dict[i:i+chunk_size] for i in range(0, len(data_dict), chunk_size)]
  # cleanup unused data to free memory
  del data_dict
  gc.collect()
  for chunk in data_chunks:
    collection.insert_many(chunk, bypass_document_validation=True)
    print('Chunk inserted.')
    # cleanup unused data to free memory
    del chunk
    gc.collect()
  print('Data inserted.')
  client.close()

if __name__ == '__main__':
  data_dict = pd.read_csv('data/aisdk-2023-05-01.csv').to_dict(orient='records')

  print('Made dictionary.')
  num_processes = 4 # do not use too many processes, it will overload the database
  batch_size = 100000 # amount of rows to insert from one process
  limit = 2000000 # total amount of data to insert into database
  data_chunks = [data_dict[i:i+batch_size] for i in range(0, limit, batch_size)]

  # cleanup unused data to free memory
  del data_dict
  gc.collect()

  print('Inserting data...')
  pool = Pool(processes=num_processes)
  pool.map(insert_data, data_chunks)
  pool.close()
  pool.join()

  print('Done.')
