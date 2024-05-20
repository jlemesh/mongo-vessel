rs.initiate({_id: "shard1ReplSet", version: 1, members: [ { _id: 0, host : "shard1:27017" }, { _id: 1, host : "shard2:27017" }, { _id: 2, host : "shard3:27017" }, ] })
