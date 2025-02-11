.PHONY: lint ruff mypy pylint format deploy test test-coverage

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

test:
	uv run pytest tests/unit autoexpense3

test-system:
	uv run pytest ./tests/system

test-stagging: test test-system
	uv run pytest ./tests/deployed_stagging

test-production: test test-system
	uv run pytest ./tests/deployed_production

test-coverage:
	uv run pytest tests autoexpense3  --cov

deploy:
	ssh root@192.53.123.44 rm -rf /app
	ssh root@192.53.123.44 git clone git@github.com:dypabo/autoexpense3.git /app
	ssh root@192.53.123.44 "cd /app ; git checkout master ; git pull ;"
	# systemd
	ssh root@192.53.123.44 cp /app/scripts/autoexpense_webapp.service /etc/systemd/system/
	ssh root@192.53.123.44 systemctl daemon-reload
	ssh root@192.53.123.44 systemctl enable autoexpense_webapp.service
	ssh root@192.53.123.44 systemctl restart autoexpense_webapp.service
