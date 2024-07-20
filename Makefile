FRONTEND_DIR := ./frontend

deploy:
	docker-compose up --build -d

deploy_backend:
	docker-compose up --build -d backend

down:
	docker-compose down

test_backend:
	pytest backend/app -vvv

test_backend_integration:
	pytest backend/app --integration -vvv

test_e2e:
	cd $(FRONTEND_DIR) && npx playwright test

test_e2e_ui:
	cd $(FRONTEND_DIR) && npx playwright test --ui

mypy:
	rm -rf .mypy_cache && mypy --install-types --non-interactive backend/app --config-file backend/mypy.ini

ruff_check:
	ruff check --select I backend/app

ruff_format:
	ruff check --select I --fix backend/app && ruff format backend/app

python_check: ruff_check mypy

jslint:
	cd $(FRONTEND_DIR) && yarn run lint


jslint-fix:
	cd $(FRONTEND_DIR) && yarn run lint:fix


jsprettier:
	cd $(FRONTEND_DIR) && yarn run prettier:fix


jsprettier-check:
	cd $(FRONTEND_DIR) && yarn run prettier


jscheck: jslint jsprettier-check


precommit: ruff_format jslint-fix jsprettier
