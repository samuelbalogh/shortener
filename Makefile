rand := $(shell echo $$RANDOM)
url = https://samu.space?${rand}
app_url = https://urlshrtr.herokuapp.com/shorten
app_url = http://127.0.0.1:5000/shorten
prod_url = https://urlshrtr.herokuapp.com/shorten
run: export APP_ENV = local

lint:
	@( \
		. ./env/bin/activate; \
		python3 -m black . --exclude env; \
	)
	
install:
	@( \
	  python3 -m venv env; \
		. ./env/bin/activate; \
		python3 -m pip install -r requirements.txt; \
	)

run:
	. ./env/bin/activate && python3 app.py

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
