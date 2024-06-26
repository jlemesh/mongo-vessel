sh.enableSharding("vessels")
use vessels
db.data.createIndex( {
  MMSI: 1,
  '# Timestamp': 1
},
{
  name: 'mmsiTimestamp'
} )
db.filtered.createIndex( {
  MMSI: 1,
  '# Timestamp': 1
},
{
  name: 'mmsiTimestamp'
} )
sh.shardCollection("vessels.data", { MMSI: 1, '# Timestamp': 1} )
sh.shardCollection("vessels.filtered", { MMSI: 1, '# Timestamp': 1} )
db.data.createIndex( {
  Longitude: 1,
  Latitude: 1,
  'Navigation status': 1,
  SOG: 1,
  ROT: 1,
  COG: 1,
  Heading: 1,
},
{
  name: 'lookupFiltering'
} )
db.filtered.createIndex( {
  MMSI: 1
})
db.filtered.createIndex( {
  '# Timestamp': 1
})
