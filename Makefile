DOCKER_COMPOSE=docker-compose
SERVICE_NAME=web


superuser:
	@echo "Creating superuser..."
	-$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python manage.py createsuperuser

run:
	@echo "Starting containers"
	-$(DOCKER_COMPOSE) up -d

stop:
	@echo "Stopping containers"
	-$(DOCKER_COMPOSE) stop

down:
	@echo "Stopping containers"
	-$(DOCKER_COMPOSE) down -v

lint:
	-$(DOCKER_COMPOSE) exec $(SERVICE_NAME) flake8
	-$(DOCKER_COMPOSE) exec $(SERVICE_NAME) isort .

test:
	-$(DOCKER_COMPOSE) exec $(SERVICE_NAME) pytest -vv
