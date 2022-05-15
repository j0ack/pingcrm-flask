MAKEFLAGS+="-j 2"

NPM=""
FLASK_DEV=FLASK_APP="app:create_app('dev')" FLASK_ENV=development

init:
	pip install -r requirements.txt
	cd static/vue && npm install
	$(FLASK_DEV) flask db upgrade

seed:
	$(FLASK_DEV) flask seed

clean:
	rm -rf app/test.db

dev-python:
	$(FLASK_DEV) flask run

dev-vue:
	@npm run --prefix static/vue/ build:dev

dev: dev-python dev-vue

test-python:
	coverage run --source app --omit=app/dev.py -m unittest discover tests
	coverage report -m --fail-under=90
