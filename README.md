# django-starter-api
![](https://img.shields.io/badge/code%20style-black-000000.svg)

A boilerplate for creating REST API with Django and Django Rest Framework.

- Gitlab CI
- Docker
- Python Black
- Flake8
- Code coverage over 93%
- Docker ready to deployment with Caddy


## Development

```bash
docker-compose -f local.yml build
docker-compose -f local.yml up
```

If you want, you can export `COMPOSE_FILE` so you don't have to write `-f local.yml` every time you want to run a docker command.
```
export COMPOSE_FILE=local.yml

docker-compose build
docker-compose up
docker-compose ps
docker-compose down
```

## Tests
```
docker-compose -f local.yml run --rm django pytest -v
docker-compose -f local.yml run --rm django pytest --cov=project tests/
```

## Create superuser

```
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

## Contributing

I'll be happily accepting pull requests from anyone.

TODO:
- Improve test coverage
- Add other CI like travis

Suggestions are welcome!


## Contributors

- [Marcos Aguayo](https://github.com/maguayo) | <marcos@aguayo.es>
