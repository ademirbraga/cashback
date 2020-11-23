# Project
> Magalutax API

## Table of Contents
* [Project Structure](#project-structure)
* [Prerequisites](#prerequisites)
* [External-Services](#external-services)
* [Auto-Documentation (_Swagger_)](#auto-Documentation-(_Swagger_))
* [Testing](#testing)
* [Migration](#migration)
* [Environment](#environment)
* [Install & Run](#install)
* [Logging](#logging)
* [Authentication](#authentication)


### Project Structure

*root*
```
├── cashback
    ├── cashback
      ├── __init__.py
      ├── asgi.py
      ├── setting.py
      ├── urls.py
      ├── wsgi.py
    ├── cashbackconfig
    ├── cashbackrevendedor    
    ├── pedido
      ├── migrations
      ├── admin.py
      ├── apps.py
      ├── models.py
      ├── serializers.py
      ├── tests.py
      ├── views.py
    ├── revendedor
    ├── statuspedido
    ├── whitelistpedido
    ├── docker-compose.yml
    ├── Dockerfile
    ├── manage.py
    ├── nose.cfg
    ├── README.md
    └── requirements.txt
```

### Prerequisites

List of all tecnologies and frameworks used in development of this project:

* [Docker Compose](https://docs.docker.com/compose/) - Setup environment for development
* [Docker](https://www.docker.com/) - Container service
* [Django](https://www.djangoproject.com) - Backend API
* [Django-rest-framework](https://www.django-rest-framework.org) - Django Rest Framework
* [Postgresql](https://www.postgresql.org) - Relational Database
* [pip](https://pypi.org/project/pip/) - Python Package Manager
* [Docker Compose](https://docs.docker.com/compose/) - Setup environment for development
* [Docker](https://www.docker.com/) - Container service



### External Services
##### Accumulated cashback [Docs](https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf= 12345678901)



### Auto-Documentation

The browsable API that REST framework provides makes it possible for your API to be entirely self describing. The documentation for each API endpoint can be provided simply by visiting the URL in your browser.
[Click here to see the documentation:](http://localhost:8000)


### Testing

The tests are created using [unittest](https://docs.python.org/3/library/unittest.html#module-unittest) and [django-nose](https://django-testing-docs.readthedocs.io/en/latest/coverage.html) for coverage purposes.
The execution of the tests uses a _Sqlite3_ database as the real application is based on it. 

**Run tests:**

```sh
python3 manage.py test
```

### Migration

THe migrations are controlled by [migrate](https://docs.djangoproject.com/en/3.1/topics/migrations/), follows a minimal example of a creation:

```bash
 $ python3 manage.py makemigrations
 $ python3 manage.py migrate
```

## Install & Run

Access the project's root folder:

**Install dependencies:**

```sh
$ pip3 install -r requirements.txt
```

**Run project:**

```sh
$ python3 manage.py runserver
```
**Run project using docker:**

```sh
$ docker-compose up -d
$ docker exec -it $( docker ps -aqf "name=cashback_web") bash
$ ./docker-entrypoint.sh --environment=dev # to run initial database migrations and create super user
```

**Authentication**
REST framework provides a number of authentication schemes out of the box, and also allows you to implement custom schemes.
[Django-Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
To use Authentication in this project within Postman:
```
User: admin
Pass: adminpass
```
Or generate token and set request header like this:
```
'Authorization': "Basic YWRtaW46YWRtaW5wYXNz"
``` 


**Down project:**

```sh
$ docker-compose down -v
```
## Logging
Django uses Python’s builtin logging module to perform system logging. [django-logging](https://docs.djangoproject.com/en/3.1/topics/logging/)

## Authors

* **Ademir Braga**

## License

...
)