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

## Deploy
Install docker and docker-compose.

Build docker:
```
sudo docker-compose -f production.yml build
```

Now install Supervisor
```
sudo apt-get install supervisor
sudo service supervisor restart
```

Now you need to create a new supervisor service, to do that go to `/etc/supervisor/conf.d`, and create the file `project.conf`. And paste this inside:
```
[program:project]
command=docker-compose -f production.yml up
directory=/home/ubuntu/project
redirect_stderr=true
autostart=true
autorestart=true
priority=10
```

Once saved run
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start project
sudo supervisorctl status project
```



## Contributing

I'll be happily accepting pull requests from anyone.

TODO:
- Improve test coverage
- Add other CI like travis

Suggestions are welcome!


## Contributors

- [Marcos Aguayo](http://marcosaguayo.com) | <marcos@aguayo.es>
