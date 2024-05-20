sh.enableSharding("vessels")
db.adminCommand( { shardCollection: "vessels.data", key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 } } )
