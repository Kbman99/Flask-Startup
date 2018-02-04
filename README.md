# Flask-Startup

## Setup

### Vanilla

- Install the requirements and setup the development environment.

	`make install && make dev`

- Create the database.

	`python manage.py initdb`

- Run the application.

	`python manage.py runserver`

- Navigate to `localhost:5000`.


### Virtual environment

``
pip install virtualenv
virtualenv venv
venv/bin/activate (venv\scripts\activate on Windows)
make install
make dev
python manage.py initdb
python manage.py runserver
``


## Deployment

The current application can be deployed with Docker [in a few commands](https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/).

```sh
cd ~/path/to/application/
docker-machine create -d virtualbox --virtualbox-memory 512 --virtualbox-cpu-count 1 dev
docker-machine env dev
eval "$(docker-machine env dev)"
docker-compose build
docker-compose up -d
docker-compose run web make dev
docker-compose run web python3 manage.py initdb
```

Then access the IP address given by `docker-machine ip dev` and it should do the trick.

## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.
