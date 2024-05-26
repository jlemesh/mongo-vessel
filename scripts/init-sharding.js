sh.enableSharding("vessels")
db.data.createIndex( {
  MMSI: 1,
  '# Timestamp': 1
},
{
  name: 'mmsiTimestamp'
} )
sh.shardCollection("vessels.data", { MMSI: 1, '# Timestamp': 1} )
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
