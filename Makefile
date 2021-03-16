rand = $(shell echo $$RANDOM)
url = https://samu.space?$(rand)
run: export APP_ENV = local

install:
	python3 -m pip install -r requirements.txt

run:
	python3 app.py

post:
	@echo "Posting $(url) to the shortener service..";
	$(eval SHORTURL = $(shell curl -s -X POST http://127.0.0.1:5000/shorten --data '{"url": "$(url)"}' --header "Content-Type: application/json"))
	@echo "The resulting short URL:"
	@echo $(SHORTURL)
