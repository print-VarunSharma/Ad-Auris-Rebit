web: gunicorn app:app --log-level=debug
web: python manage.py runserver --host 0.0.0.0 --port ${PORT}
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade
