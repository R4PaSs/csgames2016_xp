#!/bin/bash

DBDATA_CONTAINER=$(docker-compose ps | grep dbdata | awk '{print $1}')
echo "dbdata container: $DBDATA_CONTAINER"
docker run --volumes-from ${DBDATA_CONTAINER} -v $(pwd)/data:/backup ubuntu tar cvf /backup/backup.tar -C /var/lib/postgresql/ data/ -C /xp_media submission
