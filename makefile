.PHONY: test

test:
	nosetests -m'^$$' `find tests -name '*.py'`

upload:
	cp README.md README
	python sdist upload
	rm README
