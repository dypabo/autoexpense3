.PHONY: lint ruff mypy pylint format deploy

lint: ruff mypy pylint
	
format:
	uv run ruff format

ruff:
	uv run ruff check
mypy:
	uv run mypy ./autoexpense3/
	uv run mypy ./tests/
	uv run mypy ./app.py
pylint:
	uv run pylint ./autoexpense3/
	uv run pylint ./tests/
deploy:
	ssh autoexpense rm -rf /app
	ssh autoexpense git clone git@github.com:dypabo/autoexpense3.git /app
	ssh autoexpense "cd /app ; git checkout master ; git pull ;"
	# systemd
	ssh autoexpense cp /app/scripts/autoexpense_webapp.service /etc/systemd/system/
	ssh autoexpense systemctl daemon-reload
	ssh autoexpense systemctl enable autoexpense_webapp.service
	ssh autoexpense systemctl restart autoexpense_webapp.service
