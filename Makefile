all: build run

build:
	docker build -t xp containers/xp

run:
	docker run -d -t --name=xp -p 8000:8000 xp

interactive:
	docker run -i -t --name=xp -p 8000:8000 xp

dev:
	docker run -i -t --name=xp -v /data/work/XtremeProgramming_CSG16:/opt/xp -p 8000:8000 xp /bin/bash

clean:
	docker kill xp
	docker rm xp
