ENV_FILE_PATH := ./docker_compose/configs/.env
COMPOSE_FILE_PATH := ./docker_compose/docker-compose.yml

.PHONY: build
build:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) up -d --build
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) exec backend python manage.py collectstatic --noinput
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) exec backend python manage.py migrate

.PHONY: start
start:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) up -d

.PHONY: stop
stop:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) stop

.PHONY: clean
clean:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) down -v --remove-orphans

.PHONY: logs
logs:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) logs -f
