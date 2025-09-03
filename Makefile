DB_CONTAINER=h2h-db
DB_USER=postgres
DB_NAME=heart2heart

BOT_SERVICE=bot 
DB_SERVICE=postgres

.PHONY: all
all: build up

.PHONY: build
build:
	docker compose build

.PHONY: up 
up:
	docker compose up -d

.PHONY: down 
down:
	docker compose down

.PHONY: clean_db
clean_db:
	docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "TRUNCATE TABLE users CASCADE;"
	docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "TRUNCATE TABLE couples CASCADE;"

.PHONY: bot_up
bot_up:
	docker compose up $(BOT_SERVICE)

.PHONY: db_up 
db_up:
	docker compose up $(DB_SERVICE)

.PHONY: db_it
db_it:
	@docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)
