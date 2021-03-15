url = "https://samu.space"

install:
	python3 -m pip install -r requirements.txt

run:
	python3 app.py

curl:
	@echo "posting $(url) to the shortener service";
	@echo "the resulting short URL:"
	@curl -X POST http://127.0.0.1:5000/shorten --data '{"url": $(url)}' --header "Content-Type: application/json"; echo
