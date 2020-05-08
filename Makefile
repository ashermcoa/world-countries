build:
	docker-compose build

run:
	docker-compose up

run-db:
	docker exec -it db bash