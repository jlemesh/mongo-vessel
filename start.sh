#!/bin/bash

docker-compose up -d

sleep 10

docker-compose exec configsvr sh -c "mongosh < /scripts/init-configserver.js"

sleep 5

docker-compose exec shard1 sh -c "mongosh < /scripts/init-shard1ReplSet.js"
docker-compose exec shard2 sh -c "mongosh < /scripts/init-shard1ReplSet.js"
docker-compose exec shard3 sh -c "mongosh < /scripts/init-shard1ReplSet.js"

sleep 10

docker-compose exec router sh -c "mongosh < /scripts/init-router.js"
docker-compose exec router sh -c "mongosh < /scripts/init-sharding.js"
