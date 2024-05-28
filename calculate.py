import pymongo
from multiprocessing import Pool
import matplotlib.pyplot as plt
from datetime import datetime

def process_mmsis(mmsis):
  '''
  Function to process the MMSI data points and calculate the time difference between each data point

  Parameters
  ----------
  :param mmsis: list of MMSI to process

  Returns
  -------
  :return: list of time differences between each data point
  '''
  # connect to MongoDB
  client = pymongo.MongoClient("mongodb://localhost:27017")
  db = client["vessels"]
  collection = db["filtered"]
  res = []
  for mmsi in mmsis:
    data_points = collection.find({
      'MMSI': mmsi,
    }).sort( { '# Timestamp': 1 } )

    data_points = list(data_points)
    # calculate difference between each data points timestamp and save into a list
    date_fmt = '%d/%m/%Y %H:%M:%S'

    for i in range(len(data_points) - 1):
      tstamp1 = datetime.strptime(data_points[i+1]['# Timestamp'], date_fmt)
      tstamp2 = datetime.strptime(data_points[i]['# Timestamp'], date_fmt)
      res.append(int(round((tstamp1 - tstamp2).total_seconds())))

  # disconnect from MongoDB
  client.close()
  return res

if __name__ == '__main__':
  # connect to MongoDB to get distinct MMSI
  client = pymongo.MongoClient("mongodb://localhost:27017")
  db = client["vessels"]
  collection = db["filtered"]

  # get all distinct MMSI
  mmsis = collection.distinct('MMSI')

  # disconnect from MongoDB for now
  client.close()

  # process the MMSI data points in parallel
  num_processes = 4 # do not use more than 4 processes as it will overload the database
  chunk_size = len(mmsis) // num_processes
  data_chunks = [mmsis[i:i+chunk_size] for i in range(0, len(mmsis), chunk_size)]

  pool = Pool(processes=num_processes)
  res = pool.map(process_mmsis, data_chunks)

  # plot the histogram in log scale
  plt.hist([x for xs in res for x in xs], log=True)
  plt.show()

  # close the pool of worker processes
  pool.close()
  pool.join()
