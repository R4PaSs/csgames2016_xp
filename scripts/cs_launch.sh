#!/bin/bash

if [[ $PWD/ = */scripts ]];
then
	cd ..
fi

echo "Building containers..."
docker-compose build

echo "Setuping base data and data containers..."
docker-compose run xp /opt/xp/scripts/setup.sh

echo "Launching competition..."
docker-compose up

