#!/bin/bash

if [[ $PWD/ = */scripts ]];
then
	cd ..
fi

echo "Building containers..."
docker-compose build
docker-compose up db

echo "Setuping base data and data containers..."
docker-compose run xp bash /opt/xp/scripts/setup.sh

echo "Launching competition..."
docker-compose up

