
install:
	pip install -r requirements.txt; cd src/client; npm  install

python:
	cd src; uvicorn main:app --reload

react:
	cd src/client; npm start
