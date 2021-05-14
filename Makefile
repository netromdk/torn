clean:
	find . -iname __pycache__ | xargs rm -fr
	find . -iname '*.pyc' | xargs rm -f

clean-venv:
	rm -fr .venv

dist-clean: clean clean-venv

install-deps:
	.venv/bin/pip install --upgrade pip virtualenv

setup-venv: clean-venv
	virtualenv -p python3 .venv

setup: setup-venv
	.venv/bin/pip install -r requirements.txt

update-requirements: setup-venv
	.venv/bin/pip freeze > requirements.txt
