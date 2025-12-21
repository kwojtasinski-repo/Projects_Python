# How to run locally?

## Prepare application and run

Create migrations:

```sh
python manage.py migrate
```

Create static files:

```
python manage.py collectstatic
```

Add admin user:

```sh
python manage.py bootstrap_admin
```

Run server:

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

Initial admin user credentials are defined in the `.env` file:

```sh
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_PASSWORD=admin
DJANGO_ADMIN_EMAIL=admin@example.com
```

This command creates the admin user **only if it does not already exist.**

```sh
python manage.py bootstrap_admin
```

Once created, the admin credentials are stored in the database and can be changed via the Django admin panel.
Re-running the command will not overwrite an existing user.
