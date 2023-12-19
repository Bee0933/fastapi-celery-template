format:
	# format python code with black
	find . -name "*.py" ! -path "./.venv/*" | xargs black

infra:
	# run infa build
	docker-compose up -d
	