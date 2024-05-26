import pymongo
from multiprocessing import Pool
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["vessels"]
collection = db["filtered"]

# get all possible MMSI
mmsis = collection.distinct('MMSI')[:10]

print(mmsis)

# Disconnect from MongoDB
client.close()

def process_mmsis(mmsis):
  # Connect to MongoDB
  client = pymongo.MongoClient("mongodb://localhost:27017")
  db = client["vessels"]
  collection = db["filtered"]
  res = []
  for mmsi in mmsis:
    data_points = collection.find({
      'MMSI': mmsi,
    }).sort( { '# Timestamp': 1 } )
    print(f"Processing MMSI: {mmsi}")
    data_points = list(data_points)
    # calculate difference between each data points timestamp and save into a list
    fmt = '%d/%m/%Y %H:%M:%S'

    for i in range(len(data_points) - 1):
      tstamp1 = datetime.strptime(data_points[i+1]['# Timestamp'], fmt)
      tstamp2 = datetime.strptime(data_points[i]['# Timestamp'], fmt)
      res.append(int(round((tstamp1 - tstamp2).total_seconds())))

  # Disconnect from MongoDB
  client.close()
  return res

num_processes = 4
chunk_size = len(mmsis) // num_processes
data_chunks = [mmsis[i:i+chunk_size] for i in range(0, len(mmsis), chunk_size)]

input("Press Enter to continue...")
pool = Pool(processes=num_processes)

# Process the documents in parallel
res = pool.map(process_mmsis, data_chunks)
print(res)
plt.hist([x for xs in res for x in xs], log=True)
plt.show()

# Close the pool of worker processes
pool.close()
pool.join()
