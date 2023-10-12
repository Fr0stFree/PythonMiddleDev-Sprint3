ENV_FILE_PATH := ./.env
COMPOSE_FILE_PATH := ./docker-compose.yml

.PHONY: build
build:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) up -d --build

.PHONY: start-db
start-db:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) up -d db

.PHONY: stop-db
stop-db:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) stop db


.PHONY: start-backend
start-backend:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) up backend

.PHONY: stop-backend
stop-backend:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) stop backend

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
