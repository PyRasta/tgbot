
PYTEST_PARAMETERS = "."

up:
	docker compose --profile=app -p newsletter up --build -d --remove-orphans
down:
	docker compose --profile=app -p newsletter down
logs:
	docker compose --profile=app -p newsletter logs -f newsletter
migrate:
	docker compose --profile=app -p newsletter run --rm -it newsletter /bin/sh -c "alembic upgrade head"
makemigrations:
	@read -p "Migration title: " migration_title; \
	docker compose --profile=app -p newsletter exec newsletter /bin/sh -c "alembic revision --autogenerate -m '$$migration_title'"
