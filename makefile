.PHONY: test

test:
	nosetests -m'^$$' `find tests -name '*.py'`

upload:
	cp README.md README
	python setup.py sdist upload
	rm README
	rm MANIFEST
	rm -r dist
