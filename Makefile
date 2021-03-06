rand := $(shell echo $$(shuf -i 1-2000 -n 1))
url = https://xkcd.com/${rand}?some-long-text-here-because-its-supposed-to-be-a-long-url
app_url = https://urlshrtr.herokuapp.com/shorten
app_url = http://127.0.0.1:5005/shorten
prod_url = https://urlshrtr.herokuapp.com/shorten
run: export APP_ENV = local

lint:
	poetry run python3 -m black . --exclude env; \
	
install:
	poetry install
run:
	poetry run python app.py

post:
	@echo "Posting $(url) to the shortener service..";
	$(eval SHORTURL = $(shell curl -s -X POST "$(app_url)" --data '{"url": "$(url)"}' --header "Content-Type: application/json"))
	@echo "The resulting short URL:"
	@echo $(SHORTURL)

prodpost:
	@echo "Posting $(url) to the shortener service..";
	$(eval SHORTURL = $(shell curl -s -X POST "$(prod_url)" --data '{"url": "$(url)"}' --header "Content-Type: application/json"))
	@echo "The resulting short URL:"
	@echo $(SHORTURL)

.PHONY: test
test:
	poetry run python -m pytest
