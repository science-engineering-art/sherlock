
install:
	pip install -r src/requirements.txt; cd src/client; npm  install

python:
	cd src; uvicorn main:app --reload

react:
	cd src/client; npm start

run-docker: 
	cd src; docker run -d --rm --name sherlock-back -p 8000:8000 sherlock-back; cd client; docker run -d --rm --name sherlock-front -p 3000:3000 sherlock-front 

stop-docker:
	docker rmi sherlock-back; docker rmi sherlock-front
