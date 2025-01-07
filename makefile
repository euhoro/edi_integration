install:
	# Installs dependencies from requirements.txt
	pip install -r requirements.txt

format:
	# Formats code with black and isort
	black src/ tests/
	isort src/ tests/

lint:
	# Checks code style with flake8 and pylint
	flake8 src/ tests/
	pylint src/ tests/

test:
	# Runs unit tests
	pytest

#zipp:
	# pack
    #zip -r lambda-code.zip . -x "*.venv/*" "*.DS_Store" "deployment/*" "documentation/*" "*.resources/*"