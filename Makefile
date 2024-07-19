FRONTEND_DIR := ./frontend

deploy:
	docker-compose up --build -d

deploy_backend:
	docker-compose up --build -d backend

down:
	docker-compose down

test_backend:
	pytest backend/app

test_backend_integration:
	pytest backend/app --integration -vvv

test_e2e:
	cd $(FRONTEND_DIR) && npx playwright test

mypy:
	mypy backend/app --config-file backend/mypy.ini

ruff_check:
	ruff check backend/app

ruff_format:
	ruff format backend/app

jslint:
	cd $(FRONTEND_DIR) && npx eslint --ext .js,.jsx .


jslint-fix:
	cd $(FRONTEND_DIR) && npx eslint --fix --ext .js,.jsx .


jsprettier:
	cd $(FRONTEND_DIR) && npx prettier --write 'src/**/*.{js,jsx}'


jsprettier-check:
	cd $(FRONTEND_DIR) && npx prettier --check 'src/**/*.{js,jsx}'