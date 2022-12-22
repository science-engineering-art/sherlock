
install:
	pip install -r src/backend/requirements.txt; cd src/frontend; npm  install

python:
	cd src/backend; uvicorn main:app --reload

react:
	cd src/frontend; npm start

run-docker: 
	cd src/backend; docker run -d --rm --name sherlock-back -p 8000:8000 sherlock-back; cd ../frontend; docker run -d --rm --name sherlock-front -p 3000:3000 sherlock-front 

stop-docker:
	docker rmi sherlock-back; docker rmi sherlock-front
