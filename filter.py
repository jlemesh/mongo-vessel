import pymongo
from multiprocessing import Pool

mongodb_addr = "mongodb://localhost:27017"

def process_mmsis(mmsis):
  """Process MMSIs by filtering data points and inserting them into a new collection

  Parameters
  ----------
  mmsis : list
    A list of MMSI numbers to process

  Returns
  -------
  None
  """
  # connect to MongoDB
  client = pymongo.MongoClient(mongodb_addr)
  db = client["vessels"]
  collection = db["data"]
  for mmsi in mmsis:
    # query: {Latitude: {$gte: -90, $lte: 90},Longitude: {$gte: -180, $lte: 180}, 'Navigational status': {$exists: true, $ne: null, $ne: 'Unknown value'}, ROT: {$exists: true, $ne: null, $gte: 0, $lte: 720}, SOG: {$exists: true, $ne: null, $gte: 0, $lte: 102}, 'COG':{$exists: true, $ne: null, $gte: 0, $lte: 360}, Heading: {$exists: true, $ne: null, $gte: 0, $lt: 360}}
    data_points = collection.find({
      'MMSI': mmsi,
      'Latitude': {'$gt': -90, '$lt': 90},
      'Longitude': {'$gt': -180, '$lt': 180},
      'Navigational status': {'$exists': True, '$ne': None, '$ne': 'Unknown value'},
      'ROT': {'$exists': True, '$ne': None, '$gte': 0, '$lte': 720},
      'SOG': {'$exists': True, '$ne': None, '$gte': 0, '$lte': 102},
      'COG': {'$exists': True, '$ne': None, '$gte': 0, '$lte': 360},
      'Heading': {'$exists': True, '$ne': None, '$gte': 0, '$lt': 360}
    })
    print(f"Processing MMSI: {mmsi}")
    data_points = list(data_points)
    if len(data_points) >= 100:
      print(f"Inserting data points for MMSI: {mmsi}")
      db["filtered"].insert_many(data_points)
  # disconnect from MongoDB
  client.close()


if __name__ == '__main__':
  # connect to MongoDB
  client = pymongo.MongoClient(mongodb_addr)
  db = client["vessels"]
  collection = db['data']

  # get all possible MMSI
  mmsis = collection.distinct('MMSI')

  print(mmsis)

  # disconnect from MongoDB
  client.close()

  num_processes = 4
  chunk_size = len(mmsis) // num_processes
  data_chunks = [mmsis[i:i+chunk_size] for i in range(0, len(mmsis), chunk_size)]

  input("Press Enter to continue...")
  pool = Pool(processes=num_processes)
  pool.map(process_mmsis, data_chunks)
  pool.close()
  pool.join()
