FRONTEND_DIR := ./frontend

deploy:
	docker-compose up --build -d

down:
	docker-compose down

test_backend:
	pytest backend/app

test_backend_integration:
	docker-compose run --rm backend bash -c "pytest app --integration -vvv"
	make down

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