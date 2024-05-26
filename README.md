# mongo-vessel

## Start

```bash
# start
./start.sh

# check status
docker-compose exec router mongosh --port 27017
sh.status()

# stop
docker-compose down -v --remove-orphans

docker rm -f mongo-vessel-shard1-1 mongo-vessel-shard2-1 mongo-vessel-shard3-1 mongo-vessel-router-1 mongo-vessel-configsvr-1 && docker volume prune -f
```

## Load data

- Put data file in `data` directory: http://web.ais.dk/aisdata/aisdk-2023-05-01.zip
- pip install -r requirements.txt
- Activate `venv`: `source .venv/bin/activate`
- Run: `python load.py`

Data contains approximately 12 million entries and would take several hours to load depending on resources.
