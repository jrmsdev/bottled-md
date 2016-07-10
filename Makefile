.PHONY: clean
clean:
	@./setup.py clean -a
	@rm -rf __pycache__ bottled_md.egg-info/ build/ dist/ htdocs/ htmlcov/

.PHONY: test
test:
	@./setup.py test

.PHONY: test-coverage
test-coverage:
	@python3 -m coverage run --source='.' setup.py test
	@python3 -m coverage report
	@python3 -m coverage html

.PHONY: virtualenv
virtualenv:
	@python3 -m virtualenv -p python3 venv.bmd
