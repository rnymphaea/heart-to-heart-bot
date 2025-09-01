DB_CONTAINER=h2h-db
DB_USER=postgres
DB_NAME=heart2heart

.PHONY: all
all: build up

.PHONY: build
build:
	docker compose build

.PHONY: up 
up:
	docker compose up -d 

.PHONY: clean_db
clean_db:
	docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "TRUNCATE TABLE users CASCADE;"
	docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "TRUNCATE TABLE couples CASCADE;"

