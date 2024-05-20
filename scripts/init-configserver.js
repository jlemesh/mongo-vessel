rs.initiate({_id: "configReplSet", configsvr: true, version: 1, members: [ { _id: 0, host : 'configsvr:27017' } ] })
