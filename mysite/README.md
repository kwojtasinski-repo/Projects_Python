# How to run locally?

## Prepare application and run

```sh
python manage.py migrate
```

```
python manage.py collectstatic
```

```sh
python manage.py runserver
```

## Host url

Base url:

```sh
http://127.0.0.1:8000/
```

Admin panel:

```sh
http://127.0.0.1:8000/admin/
```

# How to run tests?

```sh
python manage.py test -v 2
```

## Admin panel default user

user: admin
password: admin
