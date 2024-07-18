deploy:
	docker-compose up --build -d

deploy_db:
	docker-compose up --build -d db

down:
	docker-compose down

test_backend:
	pytest backend/app

test_backend_integration:
	docker-compose run --rm backend bash -c "pytest app --integration"
	make down

mypy:
	mypy backend/app --config-file backend/mypy.ini

ruff:
	ruff check backend/app